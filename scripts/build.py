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


def write_meta_ts(path: Path, meta: dict):
    """Write a Nextra _meta.ts file from a dict."""
    lines = ["export default {"]
    for key, value in meta.items():
        escaped_key = json.dumps(key)
        if isinstance(value, dict):
            inner = ", ".join(f"{json.dumps(k)}: {json.dumps(v)}" for k, v in value.items())
            lines.append(f"  {escaped_key}: {{ {inner} }},")
        else:
            lines.append(f"  {escaped_key}: {json.dumps(value)},")
    lines.append("}")
    path.write_text("\n".join(lines) + "\n")


def build_site():
    """Generate Nextra MDX site."""
    build_nextra_site()


def build_nextra_site():
    """Generate Nextra MDX site (self-hosted on Vercel)."""
    print("\n=== Building Nextra site ===")
    config = load_config()

    pages_dir = SITE / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)

    # Clean content dirs and stale meta files under pages/ (preserve _app.tsx, index.mdx)
    for item in pages_dir.iterdir():
        if item.is_dir():
            shutil.rmtree(item)
        elif item.name.startswith("_meta."):
            item.unlink()

    # Top-level _meta.json: index + one entry per part
    top_meta = {"index": {"title": "Home", "display": "hidden"}}
    page_count = 0

    for part in config["parts"]:
        part_name = part["name"]
        part_slug = re.sub(r"[^a-z0-9]+", "-", part_name.lower()).strip("-")
        part_dir = pages_dir / part_slug
        part_dir.mkdir(parents=True, exist_ok=True)

        top_meta[part_slug] = part_name

        # Build section _meta.json for this part directory
        dir_meta = {}

        for section in part.get("sections", []):
            source_dir = section["source_dir"]
            group_name = section["group"]

            # Add a separator for the group name
            sep_key = re.sub(r"[^a-z0-9]+", "-", group_name.lower()).strip("-")
            dir_meta[f"-- {sep_key}"] = {"type": "separator", "title": group_name}

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
                for meta, body, stem in entries:
                    write_mdx(part_dir / f"{stem}.mdx", meta, body)
                    dir_meta[stem] = meta.get("title", stem)
                    page_count += 1
            else:
                for ch in section.get("chapters", []):
                    meta, body = read_clean_file(f"{source_dir}/{ch}")
                    if body:
                        write_mdx(part_dir / f"{ch}.mdx", meta, body)
                        dir_meta[ch] = meta.get("title", ch)
                        page_count += 1

        # Write the directory _meta.ts
        write_meta_ts(part_dir / "_meta.ts", dir_meta)

    # Write top-level _meta.ts
    write_meta_ts(pages_dir / "_meta.ts", top_meta)
    print(f"  {page_count} MDX pages -> site/pages/")


def escape_mdx(body: str) -> str:
    """Escape characters that MDX would interpret as JSX, outside fenced code blocks."""
    lines = body.split("\n")
    result = []
    in_code = False
    for line in lines:
        if line.startswith("```"):
            in_code = not in_code
            result.append(line)
            continue
        if in_code:
            result.append(line)
            continue
        # Escape curly braces
        line = line.replace("{", "\\{").replace("}", "\\}")
        # Escape all angle brackets — source content is plain markdown, never JSX
        line = line.replace("<", "&lt;").replace(">", "&gt;")
        # Escape import/export at start of line (MDX treats as JS)
        if re.match(r"^(import|export)\s", line):
            line = "\\" + line
        result.append(line)
    return "\n".join(result)


def write_mdx(path: Path, meta: dict, body: str):
    """Write an MDX file with Nextra-compatible frontmatter."""
    title = meta.get("title", path.stem)
    desc = re.sub(r"[*_\[\]()#>]", "", body[:200]).strip().split("\n")[0][:150]
    fm = {"title": title, "description": desc}
    if meta.get("author"):
        fm["author"] = meta["author"]
    if meta.get("published"):
        fm["date"] = meta["published"]
    frontmatter = yaml.dump(fm, default_flow_style=False, allow_unicode=True).strip()
    escaped_body = escape_mdx(body)
    path.write_text(f"---\n{frontmatter}\n---\n\n{escaped_body}\n")


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
