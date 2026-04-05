#!/usr/bin/env python3
"""Preprocess raw crawled markdown: strip boilerplate, extract metadata, add frontmatter."""

import os
import re
import sys
import yaml
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "sources"
BUILD_CLEAN = ROOT / "build" / "clean"

# Date parsing: "8th May 2024", "31st December 2023", "19th March 2025"
DATE_PATTERN = re.compile(r"(\d{1,2})(?:st|nd|rd|th)\s+(\w+)\s+(\d{4})")
MONTH_MAP = {m: i for i, m in enumerate(
    ["", "January", "February", "March", "April", "May", "June",
     "July", "August", "September", "October", "November", "December"], start=0
) if m}

# Footer markers — cut from the EARLIEST of these (scanning from bottom up)
FOOTER_PATTERNS = [
    re.compile(r"^## More recent articles"),
    re.compile(r"^## Recent articles"),
    re.compile(r"^\*\s*\[Disclosures\]"),
    re.compile(r"^###\s+Monthly briefing"),
    re.compile(r"^This is a chapter from the guide"),
    re.compile(r"^\*\*Chapters in this guide\*\*"),
]

# Secondary footer lines (appear between content and footer markers)
SECONDARY_FOOTER = [
    re.compile(r"^This is a \*\*(note|quotation)\*\*"),
    re.compile(r"^Posted \["),
    re.compile(r"^\[ \w+[\w-]*\d+ \]\("),  # tag links like [ ai1947 ](
    re.compile(r"^\*\*Next:\*\*"),
    re.compile(r"^\*\*Previous:\*\*"),
    re.compile(r"^Part of series \*\*"),
    re.compile(r"^\[ Sponsor & subscribe\]"),
    re.compile(r"^\s*Pay me to send you less"),
    re.compile(r"^\s*Sponsor me for \*\*\$"),
    re.compile(r"^\s*Created:\s+\d"),
    re.compile(r"^\s*Last modified:\s+\d"),
    re.compile(r"^\[\d+ changes?\]\("),
    re.compile(r"^.+→$"),                       # "Next chapter →" nav links
    re.compile(r"^\s*←\s*\["),                   # "← Previous chapter" nav links
]


def parse_date(text: str) -> str | None:
    """Parse 'DDth Month YYYY' into 'YYYY-MM-DD'."""
    text = text.replace(" - Link Blog", "").strip()
    m = DATE_PATTERN.search(text)
    if not m:
        return None
    day, month_name, year = int(m.group(1)), m.group(2), int(m.group(3))
    month = MONTH_MAP.get(month_name)
    if not month:
        return None
    return f"{year:04d}-{month:02d}-{day:02d}"


def extract_source_url(lines: list[str]) -> str:
    """Extract canonical URL from the [Subscribe](...) line."""
    for line in lines[:5]:
        m = re.search(r"\[Subscribe\]\((https://[^)]+)/about/#subscribe\)", line)
        if m:
            return m.group(1) + "/"
    return ""


def find_footer_start(lines: list[str]) -> int:
    """Find the line index where footer begins, scanning from bottom."""
    # First find the hard footer markers
    footer_idx = len(lines)
    for i in range(len(lines) - 1, -1, -1):
        for pat in FOOTER_PATTERNS:
            if pat.search(lines[i]):
                footer_idx = i
                break

    # Now scan backward from footer_idx to find secondary footer lines
    idx = footer_idx
    while idx > 0:
        prev = lines[idx - 1].strip()
        if not prev:  # skip blank lines
            idx -= 1
            continue
        matched = False
        for pat in SECONDARY_FOOTER:
            if pat.search(prev):
                idx -= 1
                matched = True
                break
        if not matched:
            break

    # Skip trailing blank lines before the footer
    while idx > 0 and not lines[idx - 1].strip():
        idx -= 1

    return idx


def clean_anchor_links(text: str) -> str:
    """Remove [#](url) anchor suffixes from headings."""
    return re.sub(r"\s*\[#\]\([^)]+\)", "", text)


def process_simonwillison(filepath: Path) -> dict:
    """Process a Simon Willison blog post or note."""
    lines = filepath.read_text().splitlines()
    source_url = extract_source_url(lines)

    # Strip header: lines 0-4 (weblog title, blank, subscribe, blank, sponsor)
    # Then line 5 is blank
    content_start = 6  # line index 6 is where content begins

    # Detect format: post (## Title on line 6) vs note/quotation (date on line 6)
    line6 = lines[6].strip() if len(lines) > 6 else ""

    if line6.startswith("## "):
        # Post format: ## Title, blank, date, blank, content
        title = line6.removeprefix("## ").strip()
        date_line = lines[8].strip() if len(lines) > 8 else ""
        published = parse_date(date_line)
        content_start = 10  # skip title, blank, date, blank
    else:
        # Note/quotation format: date on line 6, content from line 8
        published = parse_date(line6)
        title = None
        content_start = 8  # skip date, blank

    # Get content lines
    content_lines = lines[content_start:]

    # Find and strip footer
    footer_idx = find_footer_start(content_lines)
    content_lines = content_lines[:footer_idx]

    # Clean anchor links
    body = clean_anchor_links("\n".join(content_lines)).strip()

    # Derive title from first line of content if missing
    if not title:
        for line in content_lines:
            stripped = line.strip()
            if stripped and not stripped.startswith("!["):
                # Convert markdown links [text](url) to just text
                cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", stripped)
                # Remove remaining markdown formatting
                cleaned = re.sub(r"[*_>]", "", cleaned).strip()
                # Use first sentence or first 80 chars
                title = re.split(r"[.!?]", cleaned)[0][:80].strip()
                break
        if not title:
            title = filepath.stem.replace("-", " ").title()

    return {
        "title": title,
        "source": source_url,
        "author": "Simon Willison",
        "published": published or "unknown",
        "body": body,
    }


def process_guide(filepath: Path) -> dict:
    """Process an agentic-patterns guide chapter."""
    lines = filepath.read_text().splitlines()
    source_url = extract_source_url(lines)

    # Header: lines 0-6 (weblog title, blank, subscribe, blank, sponsor, blank, breadcrumb)
    # Line 8 = ## Chapter Title
    line8 = lines[8].strip() if len(lines) > 8 else ""
    if line8.startswith("## "):
        title = line8.removeprefix("## ").strip()
        content_start = 10  # skip title, blank
    else:
        # Fallback: some guide pages might vary
        title = filepath.stem.replace("-", " ").title()
        content_start = 8

    content_lines = lines[content_start:]

    # Find and strip footer
    footer_idx = find_footer_start(content_lines)
    content_lines = content_lines[:footer_idx]

    body = clean_anchor_links("\n".join(content_lines)).strip()

    return {
        "title": title,
        "source": source_url,
        "author": "Simon Willison",
        "published": "",  # Guide pages don't have individual dates
        "body": body,
    }


def process_frontmatter_file(filepath: Path) -> dict:
    """Process a file that already has YAML frontmatter (sysls format)."""
    text = filepath.read_text()
    if not text.startswith("---"):
        return {"title": filepath.stem, "source": "", "author": "Unknown",
                "published": "", "body": text}

    parts = text.split("---", 2)
    if len(parts) < 3:
        return {"title": filepath.stem, "source": "", "author": "Unknown",
                "published": "", "body": text}

    meta = yaml.safe_load(parts[1])
    body = parts[2].strip()

    author = meta.get("author", "Unknown")
    if isinstance(author, list):
        author = ", ".join(str(a).replace("[[@", "@").replace("]]", "") for a in author)

    published = meta.get("published", "")
    if isinstance(published, datetime):
        published = published.strftime("%Y-%m-%d")
    elif hasattr(published, "isoformat"):
        published = published.isoformat()

    return {
        "title": meta.get("title", filepath.stem),
        "source": meta.get("source", ""),
        "author": author,
        "published": str(published),
        "body": body,
    }


def write_clean(out_path: Path, meta: dict):
    """Write a cleaned markdown file with YAML frontmatter."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    frontmatter = yaml.dump({
        "title": meta["title"],
        "source": meta["source"],
        "author": meta["author"],
        "published": meta["published"],
    }, default_flow_style=False, allow_unicode=True).strip()

    out_path.write_text(f"---\n{frontmatter}\n---\n\n{meta['body']}\n")


def preprocess_all() -> list[dict]:
    """Preprocess all sources and return manifest."""
    manifest = []

    # Process agentic-patterns (skip 00-index.md)
    guide_dir = SOURCES / "agentic-patterns"
    for f in sorted(guide_dir.glob("*.md")):
        if f.name == "00-index.md":
            continue
        meta = process_guide(f)
        out = BUILD_CLEAN / "agentic-patterns" / f.name
        write_clean(out, meta)
        manifest.append({"file": f"agentic-patterns/{f.stem}", **meta})
        print(f"  guide: {f.stem} -> {meta['title']}")

    # Process simonwillison
    blog_dir = SOURCES / "simonwillison"
    for f in sorted(blog_dir.glob("*.md")):
        meta = process_simonwillison(f)
        out = BUILD_CLEAN / "simonwillison" / f.name
        write_clean(out, meta)
        manifest.append({"file": f"simonwillison/{f.stem}", **meta})
        print(f"  blog:  {f.stem} -> {meta['title'][:50]}... [{meta['published']}]")

    # Process sysls (and any other frontmatter dirs)
    for subdir in sorted(SOURCES.iterdir()):
        if subdir.name in ("agentic-patterns", "simonwillison") or not subdir.is_dir():
            continue
        for f in sorted(subdir.glob("*.md")):
            meta = process_frontmatter_file(f)
            out = BUILD_CLEAN / subdir.name / f.name
            write_clean(out, meta)
            manifest.append({"file": f"{subdir.name}/{f.stem}", **meta})
            print(f"  other: {f.stem} -> {meta['title'][:50]}...")

    return manifest


if __name__ == "__main__":
    BUILD_CLEAN.mkdir(parents=True, exist_ok=True)
    manifest = preprocess_all()
    print(f"\nPreprocessed {len(manifest)} files into {BUILD_CLEAN}")
