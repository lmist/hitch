#!/usr/bin/env bun
import { $ } from "bun";
import { existsSync, mkdirSync } from "fs";
import { join, dirname } from "path";

const root = join(dirname(import.meta.dir));
const envPath = join(root, ".env");

// load .env
if (existsSync(envPath)) {
  const lines = await Bun.file(envPath).text();
  for (const line of lines.split("\n")) {
    const [key, ...rest] = line.split("=");
    if (key && rest.length) process.env[key.trim()] = rest.join("=").trim();
  }
}

const url = process.argv[2];
const authorOverride = process.argv[3];

if (!url) {
  console.error("usage: bun scripts/add-source.ts <url> [author-dir]");
  process.exit(1);
}

const slug = url.replace(/\/$/, "").split("/").pop()!;

// determine author dir
let authorDir: string;
if (authorOverride) {
  authorDir = authorOverride;
} else if (url.includes("simonwillison.net")) {
  authorDir = "simonwillison";
} else if (url.includes("x.com") || url.includes("twitter.com")) {
  const match = url.match(/(?:x\.com|twitter\.com)\/([^/]+)/);
  authorDir = match?.[1] ?? "other";
} else {
  authorDir = "other";
}

const outDir = join(root, "sources", authorDir);
const outFile = join(outDir, `${slug}.md`);

if (existsSync(outFile)) {
  console.error(`already exists: ${outFile}`);
  console.error("delete it first if you want to re-crawl.");
  process.exit(1);
}

const accountId = process.env.CLOUDFLARE_ACCOUNT_ID;
const apiToken = process.env.CLOUDFLARE_API_TOKEN;

if (!accountId || !apiToken) {
  console.error("set CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN in .env");
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });

console.log(`crawling: ${url}`);
console.log(`  -> ${outFile}`);

const base = `https://api.cloudflare.com/client/v4/accounts/${accountId}/browser-rendering/crawl`;
const headers = {
  Authorization: `Bearer ${apiToken}`,
  "Content-Type": "application/json",
};

// start crawl
const startResp = await fetch(base, {
  method: "POST",
  headers,
  body: JSON.stringify({
    url: url.endsWith("/") ? url : url + "/",
    limit: 1,
    depth: 1,
    formats: ["markdown"],
    render: true,
  }),
});
const startData = (await startResp.json()) as any;
if (!startData.success) {
  console.error("failed to start crawl:", startData);
  process.exit(1);
}
const jobId = startData.result;
console.log(`job: ${jobId}`);

// poll
let data: any;
for (let i = 0; i < 30; i++) {
  await Bun.sleep(2000);
  const resp = await fetch(`${base}/${jobId}`, { headers });
  data = (await resp.json()) as any;
  const status = data.result.status;
  if (["completed", "errored"].includes(status)) break;
}

const records = data?.result?.records ?? [];
if (!records.length || !records[0].markdown) {
  console.error(`no markdown returned (status=${data?.result?.status})`);
  process.exit(1);
}

await Bun.write(outFile, records[0].markdown);
const title = records[0].metadata?.title ?? "untitled";
console.log(`saved: ${title} (${records[0].markdown.length} chars)`);

console.log("\nrebuilding all outputs...");
await $`make -C ${root} all`;
