#!/usr/bin/env python3
"""
Génère automatiquement les fichiers _index.md pour les manuels
à partir des PDFs trouvés dans les dossiers.
"""

import os
import yaml
from pathlib import Path


def slugify(name):
    """Convertit un nom en slug URL-friendly"""
    return name.lower().replace(" ", "-")


def find_pdfs_and_images(folder_path):
    """Trouve tous les PDFs et images dans un dossier"""
    pdfs = []
    images = []

    if not os.path.exists(folder_path):
        return pdfs, images

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            if item.lower().endswith(".pdf"):
                pdfs.append(
                    {
                        "title": item.replace(".pdf", "").replace(".PDF", ""),
                        "file": f"pdf/{folder_path.replace('content/', '').replace(os.sep, '/')}/{item}",
                        "lang": "Français",  # Détection automatique possible ici
                    }
                )
            elif item.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                images.append(
                    f"images/{folder_path.replace('content/', '').replace(os.sep, '/')}/{item}"
                )

    return pdfs, images


def generate_index_for_folder(folder_path, relative_path):
    """Génère un fichier _index.md pour un dossier"""
    pdfs, images = find_pdfs_and_images(folder_path)

    if not pdfs and not images:
        return False

    # Détecter le nom du dossier parent pour le titre
    folder_name = os.path.basename(folder_path)

    frontmatter = {
        "title": folder_name,
        "slug": slugify(folder_name),
        "description": f"Manuel de pièces pour {folder_name}",
        "draft": False,
    }

    if pdfs:
        frontmatter["manuals"] = pdfs

    if images:
        frontmatter["images"] = images

    index_path = os.path.join(folder_path, "_index.md")

    content = f"""---
{yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)}---

# {folder_name}

Manuel de pièces pour {folder_name}

## Caractéristiques



## Informations complémentaires

Pour toute question concernant ce modèle ou pour commander des pièces, n'hésitez pas à [nous contacter](/contact/).
"""

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(
        f"✓ Généré: {relative_path}/_index.md ({len(pdfs)} PDFs, {len(images)} images)"
    )
    return True


def scan_manuals_folder():
    """Scanne tous les dossiers dans content/manuels et génère les _index.md"""
    base_path = "content/manuels"

    if not os.path.exists(base_path):
        print(f"❌ Dossier {base_path} non trouvé")
        return

    count = 0

    # Parcourir récursivement
    for root, dirs, files in os.walk(base_path):
        # Ignorer les dossiers sans PDFs (dossiers de catégories)
        has_pdfs = any(f.lower().endswith(".pdf") for f in files)

        if has_pdfs:
            relative = root.replace(base_path, "").strip(os.sep)
            if generate_index_for_folder(root, relative):
                count += 1

    print(f"\n✅ {count} fichiers _index.md générés")


if __name__ == "__main__":
    scan_manuals_folder()
