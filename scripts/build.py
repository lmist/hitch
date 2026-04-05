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
SITE = ROOT / "site"


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


def resolve_section_chapters(section: dict) -> list[tuple[dict, str]]:
    """Resolve a section to a list of (meta, body) tuples."""
    source_dir = section["source_dir"]
    if section.get("order_by") == "date":
        clean_dir = CLEAN / source_dir
        if not clean_dir.exists():
            return []
        entries = []
        for f in sorted(clean_dir.glob("*.md")):
            meta, body = read_clean_file(f"{source_dir}/{f.stem}")
            if body:
                entries.append((meta, body))
        entries.sort(key=lambda e: e[0].get("published", "9999"))
        return entries
    else:
        results = []
        for ch in section.get("chapters", []):
            meta, body = read_clean_file(f"{source_dir}/{ch}")
            if body:
                results.append((meta, body))
        return results


def assemble():
    """Assemble build/book.md from cleaned files in book order."""
    print("\n=== Assembling book.md ===")
    config = load_config()
    parts_md = []

    header = f"""---
title: "{config['title']}"
subtitle: "{config['subtitle']}"
author: "Curated by {config['editor']}"
date: "{config['date']}"
---

"""
    parts_md.append(header)

    for part in config["parts"]:
        parts_md.append(f"\n# {part['name']}\n\n")

        for section in part.get("sections", []):
            entries = resolve_section_chapters(section)
            for meta, body in entries:
                title = meta.get("title", "Untitled")
                author = meta.get("author", part.get("author", ""))
                date = meta.get("published", "")
                parts_md.append(f"## {title}\n\n")
                if author or date:
                    parts_md.append(f"*{author}")
                    if date:
                        parts_md.append(f" --- {date}")
                    parts_md.append("*\n\n")
                body = re.sub(r"^(#{1,5}) ", lambda m: "##" + m.group(1) + " ", body, flags=re.MULTILINE)
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
    """Generate Mintlify MDX site."""
    build_mintlify_site()


def build_mintlify_site():
    """Generate Mintlify MDX site (deployed by Mintlify from the repo)."""
    print("\n=== Building Mintlify site ===")
    config = load_config()

    # Clean content dirs under site/
    for d in SITE.iterdir():
        if d.is_dir() and d.name not in (".mintlify", "images", "logo"):
            shutil.rmtree(d)

    navigation_tabs = []
    page_count = 0

    for part in config["parts"]:
        part_name = part["name"]
        # Use a slug for the site subdirectory
        part_slug = re.sub(r"[^a-z0-9]+", "-", part_name.lower()).strip("-")
        part_dir = SITE / part_slug
        part_dir.mkdir(parents=True, exist_ok=True)

        groups = []
        for section in part.get("sections", []):
            source_dir = section["source_dir"]
            group_name = section["group"]

            if section.get("order_by") == "date":
                clean_dir = CLEAN / source_dir
                if not clean_dir.exists():
                    continue
                entries = []
                for f in sorted(clean_dir.glob("*.md")):
                    meta, body = read_clean_file(f"{source_dir}/{f.stem}")
                    if body:
                        entries.append((meta, body, f.stem))
                entries.sort(key=lambda e: e[0].get("published", "9999"))
                pages = []
                for meta, body, stem in entries:
                    write_mdx(part_dir / f"{stem}.mdx", meta, body)
                    pages.append(f"{part_slug}/{stem}")
                    page_count += 1
                groups.append({"group": group_name, "pages": pages})
            else:
                pages = []
                for ch in section.get("chapters", []):
                    meta, body = read_clean_file(f"{source_dir}/{ch}")
                    if body:
                        write_mdx(part_dir / f"{ch}.mdx", meta, body)
                        pages.append(f"{part_slug}/{ch}")
                        page_count += 1
                groups.append({"group": group_name, "pages": pages})

        navigation_tabs.append({"tab": part_name, "groups": groups})

    docs_config = {
        "$schema": "https://mintlify.com/docs.json",
        "name": "hitch",
        "theme": "quill",
        "colors": {
            "primary": "#6366f1",
            "light": "#818cf8",
            "dark": "#4f46e5",
        },
        "navigation": {
            "tabs": navigation_tabs,
            "global": {
                "anchors": [
                    {"anchor": "github", "href": "https://github.com/lmist/hitch", "icon": "github"},
                ],
            },
        },
        "appearance": {"default": "light"},
        "footer": {
            "socials": {
                "github": "https://github.com/lmist/hitch",
            },
        },
    }
    docs_json = SITE / "docs.json"
    docs_json.write_text(json.dumps(docs_config, indent=2))
    print(f"  {page_count} MDX pages + docs.json -> site/")


def write_mdx(path: Path, meta: dict, body: str):
    """Write an MDX file with Mintlify-compatible frontmatter."""
    title = meta.get("title", path.stem)
    desc = re.sub(r"[*_\[\]()#>]", "", body[:200]).strip().split("\n")[0][:150]
    fm = {"title": title, "description": desc}
    if meta.get("author"):
        fm["author"] = meta["author"]
    if meta.get("published"):
        fm["date"] = meta["published"]
    frontmatter = yaml.dump(fm, default_flow_style=False, allow_unicode=True).strip()
    path.write_text(f"---\n{frontmatter}\n---\n\n{body}\n")


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
