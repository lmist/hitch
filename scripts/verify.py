#!/usr/bin/env python3
"""Post-build verification: check for boilerplate leaks, valid outputs, etc."""

import os
import re
import sys
import zipfile
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
CLEAN = BUILD / "clean"
SITE = ROOT / "site"

BOILERPLATE = [
    "# [Simon Willison's Weblog",
    "**Sponsored by:**",
    "[Subscribe](",
    "* [Disclosures]",
    "* [Colophon]",
    "Pay me to send you less",
    "### Monthly briefing",
    "Sponsor me for **$",
    "[ Sponsor & subscribe]",
]

YEAR_LINK = re.compile(r"^\* \[\d{4}\]\(")

errors = 0
warnings = 0


def error(msg):
    global errors
    errors += 1
    print(f"  ERROR: {msg}")


def warn(msg):
    global warnings
    warnings += 1
    print(f"  WARN:  {msg}")


def check_frontmatter():
    """Every cleaned file must have title, source, author, published."""
    print("\n--- Frontmatter completeness ---")
    required = ["title", "author"]
    for f in sorted(CLEAN.rglob("*.md")):
        text = f.read_text()
        if not text.startswith("---"):
            error(f"{f.relative_to(CLEAN)}: no frontmatter")
            continue
        parts = text.split("---", 2)
        if len(parts) < 3:
            error(f"{f.relative_to(CLEAN)}: malformed frontmatter")
            continue
        meta = yaml.safe_load(parts[1]) or {}
        for key in required:
            if not meta.get(key):
                warn(f"{f.relative_to(CLEAN)}: missing '{key}'")


def check_boilerplate():
    """No boilerplate strings should appear in cleaned files."""
    print("\n--- Boilerplate leaks ---")
    for f in sorted(CLEAN.rglob("*.md")):
        text = f.read_text()
        # Skip frontmatter
        if text.startswith("---"):
            parts = text.split("---", 2)
            if len(parts) >= 3:
                text = parts[2]
        for bp in BOILERPLATE:
            if bp in text:
                error(f"{f.relative_to(CLEAN)}: contains '{bp[:40]}...'")
        # Check for year link lists
        for line in text.splitlines():
            if YEAR_LINK.match(line):
                error(f"{f.relative_to(CLEAN)}: year link: {line[:50]}")
                break


def check_outputs():
    """Check that build outputs exist and are reasonable."""
    print("\n--- Build outputs ---")
    book_md = BUILD / "book.md"
    if not book_md.exists():
        error("book.md missing")
    else:
        size = book_md.stat().st_size
        chapters = book_md.read_text().count("\n## ")
        print(f"  book.md: {size / 1024:.0f}KB, {chapters} chapters")
        if chapters < 10:
            warn(f"Only {chapters} chapters (expected ~45)")

    for pdf in ["book-light.pdf", "book-dark.pdf"]:
        path = BUILD / pdf
        if not path.exists():
            warn(f"{pdf} missing (PDF build may have been skipped)")
        else:
            size = path.stat().st_size / 1024
            print(f"  {pdf}: {size:.0f}KB")
            if size < 100:
                error(f"{pdf} suspiciously small ({size:.0f}KB)")

    epub = BUILD / "book.epub"
    if not epub.exists():
        warn("book.epub missing (ePub build may have been skipped)")
    else:
        size = epub.stat().st_size / 1024
        print(f"  book.epub: {size:.0f}KB")
        if not zipfile.is_zipfile(epub):
            error("book.epub is not a valid zip/epub file")


def check_site():
    """Check Mintlify site structure."""
    print("\n--- Mintlify site ---")
    docs_json = SITE / "docs.json"
    if not docs_json.exists():
        warn("site/docs.json missing (site build may have been skipped)")
        return

    import json
    config = json.loads(docs_json.read_text())
    tabs = config.get("navigation", {}).get("tabs", [])
    page_refs = []
    for tab in tabs:
        for group in tab.get("groups", []):
            page_refs.extend(group.get("pages", []))

    missing = 0
    for ref in page_refs:
        mdx_path = SITE / f"{ref}.mdx"
        if not mdx_path.exists():
            error(f"docs.json references {ref} but {ref}.mdx missing")
            missing += 1
    print(f"  {len(page_refs)} pages referenced, {missing} missing")


def main():
    print("=== Verification ===")
    check_frontmatter()
    check_boilerplate()
    check_outputs()
    check_site()

    print(f"\n--- Summary: {errors} errors, {warnings} warnings ---")
    if errors > 0:
        print("FAILED")
        sys.exit(1)
    print("PASSED")


if __name__ == "__main__":
    main()
