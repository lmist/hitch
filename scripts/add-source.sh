#!/usr/bin/env bash
set -euo pipefail

# Usage: ./scripts/add-source.sh <url> [author-dir]
# Crawls a URL via Cloudflare Browser Rendering and saves it to sources/

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"

# Load .env
if [[ -f "$ROOT/.env" ]]; then
  set -a
  source "$ROOT/.env"
  set +a
fi

URL="${1:?Usage: add-source.sh <url> [author-dir]}"
SLUG=$(echo "$URL" | sed 's|/$||' | awk -F/ '{print $NF}')

# Determine author dir
if [[ -n "${2:-}" ]]; then
  AUTHOR_DIR="$2"
elif echo "$URL" | grep -q "simonwillison.net"; then
  AUTHOR_DIR="simonwillison"
elif echo "$URL" | grep -q "x.com\|twitter.com"; then
  # Extract handle from URL
  HANDLE=$(echo "$URL" | sed -E 's|https?://(x\.com\|twitter\.com)/([^/]+).*|\2|')
  AUTHOR_DIR="$HANDLE"
else
  AUTHOR_DIR="other"
fi

OUT_DIR="$ROOT/sources/$AUTHOR_DIR"
OUT_FILE="$OUT_DIR/$SLUG.md"

if [[ -f "$OUT_FILE" ]]; then
  echo "Already exists: $OUT_FILE"
  echo "Delete it first if you want to re-crawl."
  exit 1
fi

echo "Crawling: $URL"
echo "  -> $OUT_FILE"

# Ensure account ID and token are set
: "${CLOUDFLARE_ACCOUNT_ID:?Set CLOUDFLARE_ACCOUNT_ID in .env}"
: "${CLOUDFLARE_API_TOKEN:?Set CLOUDFLARE_API_TOKEN in .env}"

mkdir -p "$OUT_DIR"

python3 - "$URL" "$OUT_FILE" <<'PYEOF'
import urllib.request, json, time, sys, os

account_id = os.environ["CLOUDFLARE_ACCOUNT_ID"]
api_token = os.environ["CLOUDFLARE_API_TOKEN"]
url = sys.argv[1]
out_file = sys.argv[2]

base = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/browser-rendering/crawl"
headers = {"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"}

# Start crawl
payload = json.dumps({"url": url, "limit": 1, "depth": 1, "formats": ["markdown"], "render": True}).encode()
req = urllib.request.Request(base, data=payload, headers=headers, method="POST")
resp = json.loads(urllib.request.urlopen(req).read())
if not resp.get("success"):
    print(f"Failed to start crawl: {resp}", file=sys.stderr)
    sys.exit(1)
job_id = resp["result"]
print(f"Job: {job_id}")

# Poll
for i in range(30):
    time.sleep(2)
    req = urllib.request.Request(f"{base}/{job_id}", headers=headers)
    data = json.loads(urllib.request.urlopen(req).read())
    status = data["result"]["status"]
    if status in ("completed", "errored"):
        break

records = data["result"].get("records", [])
if not records or not records[0].get("markdown"):
    print(f"No markdown returned (status={status})", file=sys.stderr)
    sys.exit(1)

md = records[0]["markdown"]
with open(out_file, "w") as f:
    f.write(md)
title = records[0].get("metadata", {}).get("title", "Untitled")
print(f"Saved: {title} ({len(md)} chars)")
PYEOF

echo ""
echo "Rebuilding all outputs..."
cd "$ROOT" && make all
