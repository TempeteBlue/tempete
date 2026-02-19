#!/usr/bin/env python3
"""
Génère automatiquement les fichiers _index.md pour les équipements usagés
à partir des fichiers trouvés dans les dossiers.
"""

import os
import yaml


def find_files(folder_path):
    """Trouve tous les PDFs, images et fichiers YAML dans un dossier"""
    pdfs = []
    images = []
    info = {}

    if not os.path.exists(folder_path):
        return pdfs, images, info

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            if item.lower().endswith(".pdf"):
                pdfs.append(
                    {
                        "title": item.replace(".pdf", "").replace(".PDF", ""),
                        "file": item,
                    }
                )
            elif item.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                images.append(item)
            elif item.lower() == "info.yaml":
                with open(item_path, "r", encoding="utf-8") as f:
                    info = yaml.safe_load(f) or {}

    return pdfs, images, info


def generate_index_for_folder(folder_path, relative_path, has_subfolders=False):
    """Génère un fichier _index.md pour un dossier"""
    pdfs, images, info = find_files(folder_path)

    folder_name = os.path.basename(folder_path)

    # Pour un dossier de catégorie (sans fichiers mais avec sous-dossiers)
    if not pdfs and not images and not info and has_subfolders:
        frontmatter = {
            "title": folder_name,
            "description": f"Équipements usagés {folder_name}",
            "draft": False,
        }

        content = f"""---
{yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)}---

# {folder_name}

Découvrez nos équipements usagés {folder_name}.
"""

        index_path = os.path.join(folder_path, "_index.md")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"✓ Catégorie: {relative_path}/_index.md")
        return True

    # Pour un dossier avec des fichiers (équipement usagé)
    if pdfs or images or info:
        frontmatter = {
            "title": info.get("title", folder_name),
            "description": info.get("description", f"Équipement usagé {folder_name}"),
            "draft": False,
        }

        # Ajouter les specs si présentes dans info.yaml
        if "specs" in info:
            frontmatter["specs"] = info["specs"]

        # Ajouter le prix
        if "price" in info:
            frontmatter["price"] = info["price"]

        # Ajouter l'état/condition
        if "condition" in info:
            frontmatter["condition"] = info["condition"]

        # Ajouter l'année
        if "year" in info:
            frontmatter["year"] = info["year"]

        # Ajouter les heures d'utilisation
        if "hours" in info:
            frontmatter["hours"] = info["hours"]

        if pdfs:
            frontmatter["documents"] = pdfs

        if images:
            frontmatter["images"] = images

        index_path = os.path.join(folder_path, "_index.md")

        content = f"""---
{yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)}---

# {frontmatter["title"]}

{frontmatter["description"]}

## Détails

Retrouvez toutes les informations techniques et commerciales ci-dessous.

## Contact

Pour toute question ou pour planifier une visite, n'hésitez pas à [nous contacter](/contact/).
"""

        with open(index_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(
            f"✓ Équipement: {relative_path}/_index.md ({len(pdfs)} PDFs, {len(images)} images)"
        )
        return True

    return False


def scan_usages_folder():
    """Scanne tous les dossiers dans content/usages et génère les _index.md"""
    base_path = "content/usages"

    if not os.path.exists(base_path):
        print(f"❌ Dossier {base_path} non trouvé")
        return

    count = 0

    # D'abord, traiter tous les dossiers récursivement (du plus profond au plus superficiel)
    all_dirs = []
    for root, dirs, files in os.walk(base_path):
        all_dirs.append((root, dirs, files))

    # Inverser pour traiter les dossiers enfants d'abord
    all_dirs.reverse()

    for root, dirs, files in all_dirs:
        relative = root.replace(base_path, "").strip(os.sep)

        # Vérifier si ce dossier a des sous-dossiers
        has_subfolders = len(dirs) > 0

        # Vérifier si ce dossier a des fichiers
        has_files = len(files) > 0

        # Générer _index.md si nécessaire
        if has_files or has_subfolders:
            if generate_index_for_folder(root, relative, has_subfolders):
                count += 1

    print(f"\n✅ {count} fichiers _index.md générés pour les équipements usagés")


if __name__ == "__main__":
    scan_usages_folder()
