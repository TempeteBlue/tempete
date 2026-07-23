#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitaire de chargement YAML tolérant aux guillemets non fermés.

Si une ligne contient un nombre impair de guillemets doubles ("), on suppose
que le guillemet fermant a été oublié et on le rajoute automatiquement en
fin de ligne avant l'analyse YAML.
"""

import yaml


def _close_unterminated_quotes(text):
    """Ferme les guillemets doubles non terminés à la fin de chaque ligne."""
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if line.count('"') % 2 == 1:
            lines[i] = line.rstrip() + '"'
    return "\n".join(lines)


def safe_load_info(path):
    """Charge un fichier info.yaml en fermant automatiquement les guillemets
    doubles oubliés en fin de ligne. Retourne un dict (vide si fichier vide)."""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return yaml.safe_load(_close_unterminated_quotes(text)) or {}
