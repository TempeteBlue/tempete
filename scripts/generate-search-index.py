#!/usr/bin/env python3
"""
Generates a JSON search index from content files
Usage: python scripts/generate-search-index.py
"""

import json
import re
from pathlib import Path
import yaml

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

    try:
        metadata = yaml.safe_load(frontmatter_text)
        if not metadata:
            metadata = {}
    except:
        metadata = {}
        for line in frontmatter_text.split("\n"):
            if ":" in line and not line.startswith(" "):
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                metadata[key] = value

    return metadata, body


def get_info_yaml_data(folder_path):
    """Extract data from info.yaml file if it exists"""
    info_file = folder_path / "info.yaml"
    if info_file.exists():
        try:
            with open(info_file, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except:
            pass
    return None


def generate_index():
    """Generate the search index"""
    index = []
    indexed_urls = set()

    # 1. Indexer les fichiers .md existants
    for md_file in CONTENT_DIR.rglob("*.md"):
        if md_file.name.startswith("_"):
            continue

        try:
            content = md_file.read_text(encoding="utf-8")
            metadata, body = parse_frontmatter(content)

            rel_path = md_file.relative_to(CONTENT_DIR)
            # Use forward slashes for URLs (without baseURL prefix - will be relative)
            url = "/" + str(rel_path).replace("\\", "/").replace(".md", "/").replace(
                "_index/", ""
            ).replace("/index/", "/")

            # Éviter les doublons
            if url in indexed_urls:
                continue
            indexed_urls.add(url)

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

    # 2. Indexer les produits depuis info.yaml
    produits_dir = CONTENT_DIR / "produits"
    if produits_dir.exists():
        for category_dir in produits_dir.iterdir():
            if not category_dir.is_dir() or category_dir.name.startswith("_"):
                continue

            for product_dir in category_dir.iterdir():
                if not product_dir.is_dir() or product_dir.name.startswith("_"):
                    continue

                metadata = get_info_yaml_data(product_dir)
                if metadata:
                    url = f"/produits/{category_dir.name}/{product_dir.name}/"

                    if url in indexed_urls:
                        continue
                    indexed_urls.add(url)

                    entry = {
                        "title": metadata.get("title", product_dir.name),
                        "description": metadata.get("description", ""),
                        "url": url,
                        "content": metadata.get("description", ""),
                        "section": "produits",
                    }
                    index.append(entry)

    # 3. Indexer les équipements usagés depuis info.yaml
    usage_dir = CONTENT_DIR / "usage"
    if usage_dir.exists():
        for category_dir in usage_dir.iterdir():
            if not category_dir.is_dir() or category_dir.name.startswith("_"):
                continue

            for equipment_dir in category_dir.iterdir():
                if not equipment_dir.is_dir() or equipment_dir.name.startswith("_"):
                    continue

                metadata = get_info_yaml_data(equipment_dir)
                if metadata:
                    url = f"/usage/{category_dir.name}/{equipment_dir.name}/"

                    if url in indexed_urls:
                        continue
                    indexed_urls.add(url)

                    entry = {
                        "title": metadata.get("title", equipment_dir.name),
                        "description": metadata.get("description", ""),
                        "url": url,
                        "content": metadata.get("description", ""),
                        "section": "usage",
                    }
                    index.append(entry)

    # 4. Indexer les manuels depuis info.yaml ou _index.md
    manuels_dir = CONTENT_DIR / "manuels"
    if manuels_dir.exists():
        for category_dir in manuels_dir.iterdir():
            if not category_dir.is_dir() or category_dir.name.startswith("_"):
                continue

            for model_dir in category_dir.iterdir():
                if not model_dir.is_dir() or model_dir.name.startswith("_"):
                    continue

                metadata = None

                # Vérifier si c'est un dossier avec info.yaml
                metadata = get_info_yaml_data(model_dir)

                # Sinon, chercher dans _index.md
                if not metadata:
                    index_file = model_dir / "_index.md"
                    if index_file.exists():
                        try:
                            content = index_file.read_text(encoding="utf-8")
                            metadata, _ = parse_frontmatter(content)
                        except Exception as e:
                            print(f"Warning: Error reading {index_file}: {e}")

                if metadata:
                    url = f"/manuels/{category_dir.name}/{model_dir.name}/"

                    if url in indexed_urls:
                        continue
                    indexed_urls.add(url)

                    entry = {
                        "title": metadata.get("title", model_dir.name),
                        "description": metadata.get("description", ""),
                        "url": url,
                        "content": metadata.get("description", ""),
                        "section": "manuels",
                    }
                    index.append(entry)

    return index


def main():
    print("Generating search index...")

    index = generate_index()

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f"Index generated: {len(index)} pages indexed")
    print(f"File: {OUTPUT_FILE}")

    # Afficher un aperçu
    print("\nIndexed pages:")
    for entry in index[:10]:
        print(f"  - {entry['title']} ({entry['url']})")
    if len(index) > 10:
        print(f"  ... and {len(index) - 10} more")


if __name__ == "__main__":
    main()
