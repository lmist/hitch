<p align="center">
  <strong>h i t c h</strong>
</p>

<p align="center">
  <em>the hitchhiker's guide to agentic engineering</em>
</p>

<p align="center">
  <a href="https://github.com/lmist/hitch/actions/workflows/build.yml"><img src="https://github.com/lmist/hitch/actions/workflows/build.yml/badge.svg" alt="build"></a>
  <a href="https://mintlify.com"><img src="https://img.shields.io/badge/docs-mintlify-6366f1?logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNMTIgMkw0IDdWMTdMOSAyMEwyMCAxNFYzTDEyIDJaIiBmaWxsPSIjZmZmIi8+PC9zdmc+" alt="docs"></a>
  <img src="https://img.shields.io/badge/license-mit-22c55e" alt="license">
  <img src="https://img.shields.io/badge/authors-3-3b82f6" alt="authors">
  <img src="https://img.shields.io/badge/chapters-51-3b82f6" alt="chapters">
  <img src="https://img.shields.io/badge/formats-pdf%20%C2%B7%20epub%20%C2%B7%20md-f97316" alt="formats">
  <img src="https://img.shields.io/badge/make-old%20school-1a1a1a" alt="make">
</p>

---

## what is this?

a curated multi-format book compiled from the best writing on agentic engineering. guides, blog posts, courses, and community writing — one buildable collection, four output formats.

| format | use case |
|--------|----------|
| **pdf (light)** | print-friendly, palatino typeset, memoir class |
| **pdf (dark)** | catppuccin mocha theme for screen reading |
| **epub** | ibooks / kindle / any e-reader |
| **markdown** | feed into llms, import into obsidian |
| **mintlify** | browsable docs site, deployed from the repo |

one command rebuilds everything: `make all`

## contents

### simon willison
15-chapter agentic engineering patterns guide + 29 selected blog posts spanning 2019–2026.

### anthropic
6-lesson "introduction to agent skills" course from anthropic academy.

### @systematicls
"how to be a world-class agentic engineer" — originally published on x.

## dependencies

- [bun](https://bun.sh) — typescript runtime for the add-source script
- [python 3](https://python.org) + [pyyaml](https://pypi.org/project/PyYAML/) — build pipeline
- [pandoc](https://pandoc.org) — document conversion
- [texlive](https://tug.org/texlive/) (lualatex) — pdf typesetting
- [mintlify](https://mintlify.com) cli — local site preview (`mint dev`)

## quick start

```bash
# build everything
make all

# individual formats
make pdf        # light + dark pdfs
make epub       # epub for e-readers
make site       # mintlify mdx site
make verify     # run checks

# add a new post by url
make add URL=https://simonwillison.net/2025/Mar/19/vibe-coding/

# or with a custom author directory
make add URL=https://example.com/post AUTHOR=someperson

# preview the mintlify site locally
make dev
```

## project structure

```
hitch/
  sources/                  raw crawled/captured markdown
    agentic-patterns/       simon willison's guide chapters
    simonwillison/          simon willison's blog posts
    anthropic-academy/      anthropic academy course lessons
    sysls/                  @systematicls' writing
  config/
    book-order.yaml         book structure and chapter ordering
  templates/
    book.tex                latex book template (memoir + palatino)
    light.tex / dark.tex    color schemes
    epub.css                epub stylesheet
    epub-metadata.yaml      epub metadata
  scripts/
    build.py                build orchestrator
    preprocess.py           strip boilerplate, extract metadata
    verify.py               post-build validation
    add-source.ts           add new content by url (bun)
  site/                     mintlify site (mdx + docs.json)
  .github/workflows/
    build.yml               ci: build + verify all formats
  Makefile                  build targets (we old school)
```

## how it works

1. **preprocess** — raw crawled markdown gets boilerplate stripped (site headers, footers, nav, sponsor text) and yaml frontmatter injected with title, author, date, and source url.
2. **assemble** — cleaned chapters are concatenated in book order into a single `book.md` with part/chapter structure.
3. **build** — pandoc converts to pdf (via lualatex) and epub. mintlify site is generated as mdx files that mintlify deploys from the repo.
4. **verify** — automated checks for boilerplate leaks, missing frontmatter, valid outputs, and site integrity.

## adding content

```bash
make add URL=https://simonwillison.net/2026/Apr/1/some-new-post/
```

uses the cloudflare browser rendering api to crawl the page as markdown, saves it to `sources/`, and triggers a full rebuild. set `CLOUDFLARE_ACCOUNT_ID` and `CLOUDFLARE_API_TOKEN` in `.env`.

for authenticated pages (like skilljar courses), capture content via playwright and save directly to `sources/<author>/`.

to add a new author or source type, create a directory under `sources/` and add an entry to `config/book-order.yaml`.

---

## attribution

this is a curated collection. all writing belongs to its respective authors.

**simon willison** — [simonwillison.net](https://simonwillison.net)
creator of datasette, contributor to django, prolific writer on llms and developer tools. his *agentic engineering patterns* guide and blog posts form the core of this collection.

**anthropic** — [anthropic.com](https://anthropic.com)
the "introduction to agent skills" course is published by anthropic academy on skilljar.

**@systematicls** — [x.com/systematicls](https://x.com/systematicls)
author of "how to be a world-class agentic engineer," originally published as a thread on x.

## license

build tooling (scripts, templates, config) is mit licensed. source content remains the intellectual property of its respective authors and is included here for personal educational use. if you are an author and would like your content removed, please open an issue.
