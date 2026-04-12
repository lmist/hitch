#!/usr/bin/env bun
import { existsSync, mkdirSync, readdirSync } from "fs";
import { dirname, join } from "path";

type CrawlRecord = {
  url: string;
  status: string;
  metadata?: {
    title?: string;
    url?: string;
    lastModified?: string;
    status?: number;
  };
  markdown?: string;
};

type CrawlResults = {
  status: string;
  total?: number;
  finished?: number;
  records?: CrawlRecord[];
};

const root = join(dirname(import.meta.dir));
const envPath = join(root, ".env");

if (existsSync(envPath)) {
  const lines = await Bun.file(envPath).text();
  for (const line of lines.split("\n")) {
    const [key, ...rest] = line.split("=");
    if (key && rest.length) process.env[key.trim()] = rest.join("=").trim();
  }
}

const siteUrl = process.argv[2];
const authorOverride = process.argv[3];

if (!siteUrl) {
  console.error("usage: bun scripts/crawl-site.ts <site-url> [author-dir]");
  process.exit(1);
}

const site = new URL(siteUrl);
site.pathname = site.pathname.replace(/\/+$/, "") || "/";
site.search = "";
site.hash = "";

const authorDir =
  authorOverride ??
  site.hostname
    .replace(/^www\./, "")
    .replace(/\./g, "-")
    .replace(/^-+|-+$/g, "");
const outDir = join(root, "sources", authorDir);

if (existsSync(outDir) && readdirSync(outDir).length > 0) {
  console.error(`output directory is not empty: ${outDir}`);
  console.error("choose a new author dir or clear it first.");
  process.exit(1);
}

const accountId = process.env.CLOUDFLARE_ACCOUNT_ID;
const apiToken = process.env.CLOUDFLARE_API_TOKEN;

if (!accountId || !apiToken) {
  console.error("set CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN in .env");
  process.exit(1);
}

const sitemapUrl = new URL("/sitemap.xml", site.origin).toString();
const sitemap = await fetchSitemap(sitemapUrl);
const expectedCount = sitemap.urls.length;
const crawlLimit = Math.max(expectedCount + 16, 50);

mkdirSync(outDir, { recursive: true });

console.log(`crawling site: ${site.origin}`);
console.log(`saving to:    ${outDir}`);
console.log(`sitemap urls:  ${expectedCount}`);

const base = `https://api.cloudflare.com/client/v4/accounts/${accountId}/browser-rendering/crawl`;
const headers = {
  Authorization: `Bearer ${apiToken}`,
  "Content-Type": "application/json",
};

const startResp = await fetch(base, {
  method: "POST",
  headers,
  body: JSON.stringify({
    url: site.toString(),
    limit: crawlLimit,
    depth: 8,
    formats: ["markdown"],
    render: false,
    options: {
      includePatterns: [`${site.origin}/**`],
    },
  }),
});
const startData = (await startResp.json()) as { success?: boolean; result?: string; errors?: unknown };
if (!startData.success || !startData.result) {
  console.error("failed to start crawl:", JSON.stringify(startData, null, 2));
  process.exit(1);
}

const jobId = startData.result;
console.log(`job:           ${jobId}`);

let results: CrawlResults | undefined;
for (let attempt = 0; attempt < 120; attempt++) {
  await Bun.sleep(2000);
  const resp = await fetch(`${base}/${jobId}?limit=1`, { headers });
  const data = (await resp.json()) as { result?: CrawlResults };
  const status = data.result?.status;
  if (!status) continue;
  if (status !== "running") {
    results = data.result;
    break;
  }
}

if (!results) {
  console.error("crawl did not finish within 240 seconds");
  process.exit(1);
}

if (results.status !== "completed") {
  console.error(`crawl ended with status=${results.status}`);
  process.exit(1);
}

const records = await fetchAllRecords(base, jobId, headers, results.total ?? crawlLimit);
const completed = records.filter((record) => record.status === "completed" && record.markdown);

if (!completed.length) {
  console.error("crawl returned no completed markdown records");
  process.exit(1);
}

const seen = new Set<string>();
let written = 0;
for (const record of completed) {
  const url = record.metadata?.url || record.url;
  if (!url || seen.has(url)) continue;
  seen.add(url);

  const body = cleanMintlifyMarkdown(record.markdown ?? "");
  if (!body.trim()) continue;

  const title = cleanTitle(record.metadata?.title || filenameFromUrl(url));
  const published = sitemap.lastmodByUrl.get(url)?.slice(0, 10) ?? "";
  const filename = uniqueFilename(filenameFromUrl(url), seen, outDir);
  const content = `---\ntitle: ${yamlString(title)}\nsource: ${yamlString(url)}\nauthor: ${yamlString("CAMEL-AI OASIS Docs")}\npublished: ${yamlString(published)}\n---\n\n${body}\n`;

  await Bun.write(join(outDir, filename), content);
  written += 1;
}

console.log(`written files: ${written}`);
if (expectedCount && written < expectedCount) {
  console.warn(`warning: sitemap listed ${expectedCount} URLs but only ${written} markdown files were written`);
}

function cleanTitle(title: string): string {
  return title.replace(/\s+-\s+OASIS$/, "").trim();
}

function cleanMintlifyMarkdown(markdown: string): string {
  let lines = markdown.replace(/\r\n/g, "\n").split("\n");

  const start = lines.findIndex((line) => /^#\s+\S/.test(line.trim()));
  if (start >= 0) lines = lines.slice(start);

  const endMarkers = [/^⌘I$/, /^\[x\]\(https:\/\/x\.com\//, /^\[Powered by/];
  const end = lines.findIndex((line) => endMarkers.some((pattern) => pattern.test(line.trim())));
  if (end >= 0) lines = lines.slice(0, end);

  lines = lines.filter((line) => !/^\[[^\]]*]\(#.*\)$/.test(line.trim()));
  lines = lines.filter((line) => !/^#{1,6}\s*$/.test(line.trim()));

  const compacted: string[] = [];
  let blankRun = 0;
  for (const line of lines) {
    if (!line.trim()) {
      blankRun += 1;
      if (blankRun > 1) continue;
    } else {
      blankRun = 0;
    }
    compacted.push(line);
  }

  return compacted.join("\n").trim();
}

function filenameFromUrl(url: string): string {
  const parsed = new URL(url);
  const rawPath = decodeURIComponent(parsed.pathname).replace(/\/+$/, "");
  if (!rawPath || rawPath === "/") return "index";
  const parts = rawPath
    .slice(1)
    .split("/")
    .filter(Boolean)
    .map((part) =>
      part
        .replace(/[^a-zA-Z0-9._-]+/g, "-")
        .replace(/^-+|-+$/g, "")
        .toLowerCase(),
    )
    .filter(Boolean);
  return parts.join("--") || "page";
}

function uniqueFilename(base: string, seenUrls: Set<string>, directory: string): string {
  let candidate = `${base}.md`;
  let suffix = 2;
  while (existsSync(join(directory, candidate))) {
    candidate = `${base}-${suffix}.md`;
    suffix += 1;
  }
  return candidate;
}

async function fetchAllRecords(
  base: string,
  jobId: string,
  headers: Record<string, string>,
  total: number,
): Promise<CrawlRecord[]> {
  const pageSize = 50;
  const records: CrawlRecord[] = [];

  for (let cursor = 0; cursor < Math.max(total, pageSize); cursor += pageSize) {
    const resp = await fetch(
      `${base}/${jobId}?status=completed&limit=${pageSize}&cursor=${cursor}`,
      { headers },
    );
    const data = (await resp.json()) as { result?: CrawlResults };
    const chunk = data.result?.records ?? [];
    if (!chunk.length) break;
    records.push(...chunk);
    if (chunk.length < pageSize) break;
  }

  return records;
}

async function fetchSitemap(sitemapUrl: string): Promise<{
  urls: string[];
  lastmodByUrl: Map<string, string>;
}> {
  try {
    const resp = await fetch(sitemapUrl);
    if (!resp.ok) {
      return { urls: [], lastmodByUrl: new Map() };
    }
    const xml = await resp.text();
    const matches = [...xml.matchAll(/<url>\s*<loc>(.*?)<\/loc>\s*(?:<lastmod>(.*?)<\/lastmod>)?/gs)];
    const urls: string[] = [];
    const lastmodByUrl = new Map<string, string>();
    for (const match of matches) {
      const loc = match[1]?.trim();
      const lastmod = match[2]?.trim() ?? "";
      if (!loc) continue;
      urls.push(loc);
      if (lastmod) lastmodByUrl.set(loc, lastmod);
    }
    return { urls, lastmodByUrl };
  } catch {
    return { urls: [], lastmodByUrl: new Map() };
  }
}

function yamlString(value: string): string {
  return JSON.stringify(value);
}
