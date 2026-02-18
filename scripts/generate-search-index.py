#!/usr/bin/env python3
"""
Generates a JSON search index from content files
Usage: python scripts/generate-search-index.py
"""

import json
import re
from pathlib import Path

CONTENT_DIR = Path("content")
OUTPUT_FILE = Path("static/search-index.json")


def parse_frontmatter(content):
    """Simple YAML frontmatter parser"""
    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    frontmatter_text = parts[1].strip()
    body = parts[2].strip()

    metadata = {}
    for line in frontmatter_text.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            metadata[key] = value

    return metadata, body


def generate_index():
    """Generate the search index"""
    index = []

    for md_file in CONTENT_DIR.rglob("*.md"):
        if md_file.name.startswith("_"):
            continue

        try:
            content = md_file.read_text(encoding="utf-8")
            metadata, body = parse_frontmatter(content)

            rel_path = md_file.relative_to(CONTENT_DIR)
            # Use forward slashes for URLs and include baseURL prefix
            url = "/tempete/" + str(rel_path).replace("\\", "/").replace(
                ".md", "/"
            ).replace("_index/", "")

            entry = {
                "title": metadata.get("title", md_file.stem),
                "description": metadata.get("description", ""),
                "url": url,
                "content": body[:500] if body else "",
                "section": str(rel_path).replace("\\", "/").split("/")[0],
            }

            index.append(entry)

        except Exception as e:
            print(f"Warning: Error with {md_file}: {e}")

    return index


def main():
    print("Generating search index...")

    index = generate_index()

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f"Index generated: {len(index)} pages indexed")
    print(f"File: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
