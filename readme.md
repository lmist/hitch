<p align="center">
  <strong>h i t c h</strong>
</p>

<p align="center">
  <em>the hitchhiker's guide to agentic engineering</em>
</p>

<p align="center">
  <a href="https://github.com/lmist/hitch/actions/workflows/build.yml"><img src="https://github.com/lmist/hitch/actions/workflows/build.yml/badge.svg" alt="build"></a>
</p>

<p align="center">
  pdf (light &amp; dark) · epub · markdown · mintlify site
</p>

---

## what is this?

a curated multi-format book compiled from the best writing on agentic engineering. guides, blog posts, courses, and community writing — one buildable collection, five output formats.

| format | use case |
|--------|----------|
| **pdf (light)** | print-friendly, palatino typeset, memoir class |
| **pdf (dark)** | catppuccin mocha theme for screen reading |
| **epub** | ibooks / kindle / any e-reader |
| **markdown** | feed into llms, import into obsidian |
| **static site** | browsable web version via github pages |

one command rebuilds everything: `make all`

## contents

### part i — agentic engineering patterns
simon willison's comprehensive guide to working with coding agents like claude code and codex. 15 chapters covering principles, workflows, testing, and annotated prompts.

### part ii — blog posts
29 selected posts by simon willison spanning 2019–2026, from "the perfect commit" to "2025: the year in llms." chronologically ordered.

### part iii — agent skills
anthropic academy's 6-lesson course on building, configuring, and sharing skills in claude code.

### part iv — other voices
community perspectives, starting with @systematicls' "how to be a world-class agentic engineer."

## dependencies

- [bun](https://bun.sh) — typescript runtime for the add-source script
- [python 3](https://python.org) + [pyyaml](https://pypi.org/project/PyYAML/) — build pipeline
- [pandoc](https://pandoc.org) — document conversion
- [texlive](https://tug.org/texlive/) (lualatex) — pdf typesetting
- [mintlify](https://mintlify.com) cli (optional) — web site preview

## quick start

```bash
# build everything
make all

# individual formats
make pdf        # light + dark pdfs
make epub       # epub for e-readers
make site       # static html site
make verify     # run checks

# add a new post by url
make add URL=https://simonwillison.net/2025/Mar/19/vibe-coding/

# or with a custom author directory
make add URL=https://example.com/post AUTHOR=someperson

# preview the site locally
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
  .github/workflows/
    build.yml               ci: build all formats, deploy to pages
  Makefile                  build targets (we old school)
```

## how it works

1. **preprocess** — raw crawled markdown gets boilerplate stripped (site headers, footers, nav, sponsor text) and yaml frontmatter injected with title, author, date, and source url.
2. **assemble** — cleaned chapters are concatenated in book order into a single `book.md` with part/chapter structure.
3. **build** — pandoc converts to pdf (via lualatex), epub, and a static html site with sidebar nav and dark mode support.
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
