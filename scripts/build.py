#!/usr/bin/env python3
"""Main build orchestrator: preprocess, assemble, and build all output formats."""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
CLEAN = BUILD / "clean"
CONFIG = ROOT / "config"
TEMPLATES = ROOT / "templates"
SITE = BUILD / "site"


def load_config():
    with open(CONFIG / "book-order.yaml") as f:
        return yaml.safe_load(f)


def read_clean_file(rel_path: str) -> tuple[dict, str]:
    """Read a cleaned markdown file, return (frontmatter_dict, body)."""
    path = CLEAN / f"{rel_path}.md"
    if not path.exists():
        print(f"  WARNING: missing {path}")
        return {}, ""
    text = path.read_text()
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            meta = yaml.safe_load(parts[1]) or {}
            body = parts[2].strip()
            return meta, body
    return {}, text


def preprocess():
    """Run the preprocessing step."""
    print("=== Preprocessing ===")
    CLEAN.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "preprocess.py")],
        cwd=str(ROOT),
    )
    if result.returncode != 0:
        print("Preprocessing failed!")
        sys.exit(1)


def assemble():
    """Assemble build/book.md from cleaned files in book order."""
    print("\n=== Assembling book.md ===")
    config = load_config()
    parts_md = []

    # YAML metadata for pandoc
    header = f"""---
title: "{config['title']}"
subtitle: "{config['subtitle']}"
author: "Curated by {config['editor']}"
date: "{config['date']}"
---

"""
    parts_md.append(header)

    for part in config["parts"]:
        part_name = part["name"]
        parts_md.append(f"\n# {part_name}\n\n")

        if part.get("order_by") == "date":
            # Collect all files from source_dir, sort by date
            source_dir = part["source_dir"]
            clean_dir = CLEAN / source_dir
            if not clean_dir.exists():
                continue
            entries = []
            for f in clean_dir.glob("*.md"):
                meta, body = read_clean_file(f"{source_dir}/{f.stem}")
                if body:
                    entries.append((meta, body, f.stem))
            # Sort by published date
            entries.sort(key=lambda e: e[0].get("published", "9999"))
            for meta, body, stem in entries:
                title = meta.get("title", stem)
                author = meta.get("author", "")
                date = meta.get("published", "")
                parts_md.append(f"## {title}\n\n")
                if author or date:
                    parts_md.append(f"*{author}")
                    if date:
                        parts_md.append(f" --- {date}")
                    parts_md.append("*\n\n")
                # Demote headings: ## -> ###, ### -> ####, etc.
                body = re.sub(r"^(#{2,5}) ", lambda m: "#" + m.group(1) + " ", body, flags=re.MULTILINE)
                parts_md.append(body + "\n\n")
        else:
            # Explicit chapter list
            chapters = part.get("chapters", [])
            source_dir = part.get("source_dir", "")
            for ch in chapters:
                if isinstance(ch, dict):
                    sd = ch.get("source_dir", source_dir)
                    fname = ch["file"]
                else:
                    sd = source_dir
                    fname = ch
                meta, body = read_clean_file(f"{sd}/{fname}")
                if not body:
                    continue
                title = meta.get("title", fname)
                author = meta.get("author", part.get("author", ""))
                date = meta.get("published", "")
                parts_md.append(f"## {title}\n\n")
                if author or date:
                    parts_md.append(f"*{author}")
                    if date:
                        parts_md.append(f" --- {date}")
                    parts_md.append("*\n\n")
                body = re.sub(r"^(#{2,5}) ", lambda m: "#" + m.group(1) + " ", body, flags=re.MULTILINE)
                parts_md.append(body + "\n\n")

    book_md = "".join(parts_md)
    out = BUILD / "book.md"
    out.write_text(book_md)
    chapter_count = book_md.count("\n## ")
    print(f"  Written {out} ({len(book_md)} chars, {chapter_count} chapters)")
    return out


def build_pdf(book_md: Path, mode: str):
    """Build PDF using pandoc + xelatex."""
    print(f"\n=== Building PDF ({mode}) ===")
    color_defs = TEMPLATES / f"{mode}.tex"
    output = BUILD / f"book-{mode}.pdf"
    cmd = [
        "pandoc", str(book_md),
        "-o", str(output),
        "--pdf-engine=lualatex",
        f"--template={TEMPLATES / 'book.tex'}",
        f"-V", f"color-defs={color_defs}",
        "--toc", "--toc-depth=2",
        "--top-level-division=chapter",
        "-V", "documentclass=memoir",
    ]
    print(f"  {' '.join(cmd[:6])}...")
    result = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  FAILED: {result.stderr[-500:]}")
        return False
    size = output.stat().st_size / 1024
    print(f"  OK: {output.name} ({size:.0f}KB)")
    return True


def build_epub(book_md: Path):
    """Build ePub using pandoc."""
    print("\n=== Building ePub ===")
    output = BUILD / "book.epub"
    cmd = [
        "pandoc", str(book_md),
        "-o", str(output),
        f"--css={TEMPLATES / 'epub.css'}",
        "--toc", "--toc-depth=2",
        "--top-level-division=chapter",
        "--epub-chapter-level=2",
    ]
    meta_file = TEMPLATES / "epub-metadata.yaml"
    if meta_file.exists():
        cmd.append(f"--epub-metadata={meta_file}")
    print(f"  {' '.join(cmd[:6])}...")
    result = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  FAILED: {result.stderr[-500:]}")
        return False
    size = output.stat().st_size / 1024
    print(f"  OK: {output.name} ({size:.0f}KB)")
    return True


def build_site():
    """Generate a static HTML site from book.md using pandoc."""
    print("\n=== Building static site ===")
    site_out = BUILD / "site"
    if site_out.exists():
        shutil.rmtree(site_out)
    site_out.mkdir(parents=True)

    book_md = BUILD / "book.md"
    index_html = site_out / "index.html"

    # Build a self-contained HTML site with pandoc
    cmd = [
        "pandoc", str(book_md),
        "-o", str(index_html),
        "--standalone",
        "--toc", "--toc-depth=2",
        "--top-level-division=chapter",
        "--metadata", "title=the hitchhiker's guide to agentic engineering",
        "--css", "style.css",
        "--template", str(TEMPLATES / "site.html"),
    ]
    result = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  FAILED: {result.stderr[-500:]}")
        return False

    # Copy the CSS
    css_src = TEMPLATES / "site.css"
    if css_src.exists():
        shutil.copy(css_src, site_out / "style.css")

    print(f"  OK: {index_html} ({index_html.stat().st_size / 1024:.0f}KB)")


def main():
    parser = argparse.ArgumentParser(description="Build the Hitch book")
    parser.add_argument("--preprocess", action="store_true")
    parser.add_argument("--pdf", action="store_true")
    parser.add_argument("--epub", action="store_true")
    parser.add_argument("--site", action="store_true")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()

    if args.all:
        args.preprocess = args.pdf = args.epub = args.site = args.verify = True

    if not any([args.preprocess, args.pdf, args.epub, args.site, args.verify]):
        args.all = True
        args.preprocess = args.pdf = args.epub = args.site = args.verify = True

    BUILD.mkdir(parents=True, exist_ok=True)

    if args.preprocess:
        preprocess()

    book_md = assemble()

    if args.pdf:
        build_pdf(book_md, "light")
        build_pdf(book_md, "dark")

    if args.epub:
        build_epub(book_md)

    if args.site:
        build_site()

    if args.verify:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "verify.py")],
            cwd=str(ROOT),
        )
        if result.returncode != 0:
            sys.exit(1)

    print("\n=== Build complete ===")


if __name__ == "__main__":
    main()
