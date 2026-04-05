<p align="center">
  <strong>H I T C H</strong>
</p>

<p align="center">
  <em>A curated reader on agentic engineering &mdash; patterns, practices, and perspectives from the people building with AI coding agents.</em>
</p>

<p align="center">
  PDF (light &amp; dark) &middot; ePub &middot; Markdown &middot; Mintlify site
</p>

---

## What is this?

Hitch is a multi-format book compiled from the best writing on agentic engineering. It pulls together guides, blog posts, courses, and community writing into a single, buildable collection that outputs:

| Format | Use case |
|--------|----------|
| **PDF (light)** | Print-friendly, Palatino typeset, Memoir class |
| **PDF (dark)** | Catppuccin Mocha theme for screen reading |
| **ePub** | iBooks / Kindle / any e-reader |
| **Markdown** | Feed into LLMs, import into Obsidian |
| **Mintlify site** | Browsable web version |

One command rebuilds everything: `make all`

## Contents

### Part I --- Agentic Engineering Patterns
Simon Willison's comprehensive guide to working with coding agents like Claude Code and Codex. 15 chapters covering principles, workflows, testing, and annotated prompts.

### Part II --- Blog Posts
29 selected posts by Simon Willison spanning 2019--2026, from "The Perfect Commit" to "2025: The Year in LLMs." Chronologically ordered.

### Part III --- Agent Skills
Anthropic Academy's 6-lesson course on building, configuring, and sharing Skills in Claude Code.

### Part IV --- Other Voices
Community perspectives, starting with @systematicls' "How To Be A World-Class Agentic Engineer."

## Quick start

```bash
# Prerequisites: pandoc, lualatex (TeX Live), python3, pyyaml
# Optional: mint (Mintlify CLI) for the web version

# Build everything
make all

# Or build individual formats
make pdf        # light + dark PDFs
make epub       # ePub for e-readers
make site       # Mintlify site (then: make dev)

# Add a new post by URL
./scripts/add-source.sh https://simonwillison.net/2025/Mar/19/vibe-coding/

# Preview the Mintlify site
make dev
```

## Project structure

```
hitch/
  sources/                  Raw crawled/captured markdown (the archive)
    agentic-patterns/       Simon Willison's guide chapters
    simonwillison/          Simon Willison's blog posts
    anthropic-academy/      Anthropic Academy course lessons
    sysls/                  @systematicls' writing
  config/
    book-order.yaml         Book structure and chapter ordering
  templates/
    book.tex                LaTeX book template (Memoir + Palatino)
    light.tex / dark.tex    Color schemes
    epub.css                ePub stylesheet
    epub-metadata.yaml      ePub metadata
  scripts/
    build.py                Build orchestrator
    preprocess.py           Strip boilerplate, extract metadata
    verify.py               Post-build validation
    add-source.sh           Add new content by URL
  Makefile                  Build targets
```

## How it works

1. **Preprocess** --- Raw crawled markdown gets boilerplate stripped (site headers, footers, nav, sponsor text) and YAML frontmatter injected with title, author, date, and source URL.
2. **Assemble** --- Cleaned chapters are concatenated in book order into a single `book.md` with part/chapter structure.
3. **Build** --- Pandoc converts to PDF (via LuaLaTeX) and ePub. Mintlify site is generated from the cleaned files.
4. **Verify** --- Automated checks for boilerplate leaks, missing frontmatter, valid outputs, and site integrity.

## Adding content

Drop a URL and rebuild:

```bash
./scripts/add-source.sh <url> [author-dir]
```

This uses the Cloudflare Browser Rendering API to crawl and convert the page to markdown, saves it to `sources/`, and triggers a full rebuild. Set `CLOUDFLARE_ACCOUNT_ID` and `CLOUDFLARE_API_TOKEN` in `.env`.

For authenticated pages (like Skilljar courses), capture content via Playwright and save directly to `sources/<author>/`.

To add a new author or source type, create a directory under `sources/` and add an entry to `config/book-order.yaml`.

---

## Attribution

This is a curated collection. All writing belongs to its respective authors.

**Simon Willison** --- [simonwillison.net](https://simonwillison.net)
Creator of Datasette, contributor to Django, prolific writer on LLMs and developer tools. His *Agentic Engineering Patterns* guide and blog posts form the core of this collection. Licensed under his site's terms.

**Anthropic** --- [anthropic.com](https://anthropic.com)
The "Introduction to Agent Skills" course is published by Anthropic Academy on Skilljar. Content reproduced here for personal reference.

**@systematicls** --- [x.com/systematicls](https://x.com/systematicls)
Author of "How To Be A World-Class Agentic Engineer," originally published as a thread on X.

## License

This repository contains the build tooling (scripts, templates, config) and curated source material. The build tooling is MIT licensed. The source content remains the intellectual property of its respective authors and is included here for personal educational use. If you are an author and would like your content removed, please open an issue.
