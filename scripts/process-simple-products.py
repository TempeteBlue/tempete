#!/usr/bin/env python3
"""
Script pour traiter les dossiers de produits simples
Structure attendue: content/produits/<produit>/
  - info.yaml (métadonnées)
  - *.jpg, *.png, *.jpeg (images)
  - *.pdf (documents/fiches techniques)

Le script copie les images vers static/images/produits/ et génère le fichier .md
"""

import os
import yaml
from pathlib import Path
import shutil

CONTENT_DIR = Path("content/produits")
STATIC_PDF_DIR = Path("static/pdf/produits")
STATIC_IMAGES_DIR = Path("static/images/produits")


def process_product_folders():
    """Traite tous les dossiers de produits"""

    for product_dir in CONTENT_DIR.iterdir():
        if not product_dir.is_dir() or product_dir.name.startswith("_"):
            continue

        yaml_file = product_dir / "info.yaml"

        if not yaml_file.exists():
            continue

        # Lire les métadonnées
        with open(yaml_file, "r", encoding="utf-8") as f:
            metadata = yaml.safe_load(f)

        product_name = product_dir.name
        pdf_target_dir = STATIC_PDF_DIR / product_name
        pdf_target_dir.mkdir(parents=True, exist_ok=True)

        # Copier les images
        images_data = []
        image_target_dir = STATIC_IMAGES_DIR / product_name
        image_target_dir.mkdir(parents=True, exist_ok=True)
        image_files = (
            list(product_dir.glob("*.jpg"))
            + list(product_dir.glob("*.jpeg"))
            + list(product_dir.glob("*.png"))
            + list(product_dir.glob("*.webp"))
        )
        image_files = [f for f in image_files if f.name != "desktop.ini"]

        for img_file in image_files:
            target_img = image_target_dir / img_file.name
            shutil.copy2(img_file, target_img)
            images_data.append(f"images/produits/{product_name}/{img_file.name}")
            print(f"  🖼️ Copié: {img_file.name}")

        # Copier les PDFs et créer la liste des documents
        documents_data = []
        pdf_files = list(product_dir.glob("*.pdf"))
        pdf_files = [f for f in pdf_files if f.name != "desktop.ini"]

        for pdf_file in pdf_files:
            target_pdf = pdf_target_dir / pdf_file.name
            shutil.copy2(pdf_file, target_pdf)

            # Utiliser le nom du fichier (sans extension) comme titre (conserver les tirets)
            pdf_title = pdf_file.stem

            documents_data.append(
                {
                    "title": pdf_title,
                    "file": f"pdf/produits/{product_name}/{pdf_file.name}",
                }
            )
            print(f"  📄 Copié: {pdf_file.name}")

        # Générer le fichier markdown
        md_content = generate_markdown(
            metadata, product_name, images_data, documents_data
        )
        md_file = product_dir / "index.md"

        with open(md_file, "w", encoding="utf-8") as f:
            f.write(md_content)

        print(f"  ✓ Généré: {md_file}")


def generate_markdown(metadata, product_name, images_data, documents_data):
    """Génère le contenu markdown"""

    if images_data is None:
        images_data = []

    frontmatter = {
        "title": metadata.get("title", product_name),
        "slug": product_name,
        "description": metadata.get("description", f"Produit {product_name}"),
        "date": metadata.get("date", "2024-01-01"),
        "draft": False,
    }

    # Catégories
    if "categories" in metadata:
        frontmatter["categories"] = metadata["categories"]

    # Prix
    if "price" in metadata:
        frontmatter["price"] = metadata["price"]
    if "price_note" in metadata:
        frontmatter["price_note"] = metadata["price_note"]

    # Images
    if images_data:
        frontmatter["images"] = images_data

    # Documents/PDFs
    if documents_data:
        frontmatter["documents"] = documents_data

    # Specs
    if "specs" in metadata:
        frontmatter["specs"] = metadata["specs"]

    # SKU
    if "sku" in metadata:
        frontmatter["sku"] = metadata["sku"]

    # In stock
    if "in_stock" in metadata:
        frontmatter["in_stock"] = metadata["in_stock"]

    yaml_content = yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)

    # Générer le contenu
    content = f"""---
{yaml_content}---

{metadata.get("description", "")}

"""

    # Ajouter les specs dans le contenu
    if "specs" in metadata:
        content += "## Caractéristiques\n\n"
        for key, value in metadata["specs"].items():
            content += f"- **{key}**: {value}\n"
        content += "\n"

    content += """## Informations complémentaires

"""

    if "sku" in metadata:
        content += f"- **Référence (SKU)**: {metadata['sku']}\n"

    content += f"- **Disponibilité**: {'En stock' if metadata.get('in_stock', True) else 'Sur commande'}\n"

    if "garantie" in metadata.get("specs", {}):
        content += f"- **Garantie**: {metadata['specs']['garantie']}\n"
    else:
        content += "- **Garantie**: Voir détails en magasin\n"

    content += f"""

Pour plus d'informations ou pour commander ce produit, [contactez-nous](/contact/?produit={product_name}).
"""

    return content


if __name__ == "__main__":
    print("📦 Traitement des dossiers de produits...")
    process_product_folders()
    print("\n✅ Traitement terminé!")
