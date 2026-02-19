# Structure des dossiers pour produits et équipements usagés

## Comment ajouter un produit ou un équipement usagé

### Pour les Produits

Créer un dossier dans `content/produits/<nom-du-produit>/` avec :

1. **info.yaml** - Métadonnées du produit (voir exemple ci-dessous)
2. **Images** - Fichiers .jpg, .jpeg, .png, .webp (optionnel)
3. **PDFs** - Fiches techniques, manuels (optionnel)

#### Exemple info.yaml pour un produit :

```yaml
title: "Blizzard B72c"
description: "Souffleuse à neige professionnelle 72 pouces"
categories:
  - "Souffleuses"
  - "Professionnel"
price: "18 999 $"
price_note: "Prix avant taxes"
sku: "BLZ-B72C-2026"
in_stock: true
date: "2024-01-15"
specs:
  Largeur de travail: "72 pouces (183 cm)"
  Hauteur d'attaque: "30 pouces (76 cm)"
  Poids: "1 200 lbs (544 kg)"
  Garantie: "3 ans / 2000 heures"
```

### Pour les Équipements Usagés

Créer un dossier dans `content/usages/<nom-equipement>/` avec :

1. **info.yaml** - Métadonnées de l'équipement (voir exemple ci-dessous)
2. **Images** - Fichiers .jpg, .jpeg, .png, .webp (optionnel)
3. **PDFs** - Fiches techniques, factures d'entretien (optionnel)

#### Exemple info.yaml pour un équipement usagé :

```yaml
title: "Souffleuse Industrielle Pro 2019"
description: "Souffleuse industrielle usagée - Excellente condition"
categories:
  - "Souffleuses"
  - "Usagé"
price: "8 500 $"
price_note: "Prix négociable - Financement disponible"
condition: "Excellent"
year: "2019"
hours: "1 250"
sku: "USED-SOUF-2019-001"
date: "2024-02-10"
specs:
  Largeur de travail: "84 pouces (213 cm)"
  Heures d'utilisation: "1 250 heures"
  État général: "Excellent"
  Garantie: "6 mois pièces et main-d'œuvre"
```

## Ce qui se passe automatiquement

Lors du déploiement (GitHub Actions), les scripts Python :

1. **Copient les images** vers `static/images/produits/` ou `static/images/usages/`
2. **Copient les PDFs** vers `static/pdf/produits/` ou `static/pdf/usages/`
3. **Génèrent le fichier** `index.md` avec tout le contenu frontmatter
4. **Mettent à jour les index** des catégories

## Exemples créés

- `content/produits/blizzard-b72c/` - Souffleuse professionnelle neuve
- `content/produits/blizzard-b64c/` - Souffleuse professionnelle neuve
- `content/usages/souffleuse-industrielle-2019/` - Équipement usagé
- `content/usages/balais-municipal-2020/` - Équipement usagé

## Champs disponibles

### Champs communs (produits et usagés)

- `title` - Nom du produit/équipement
- `description` - Description courte
- `categories` - Liste des catégories
- `price` - Prix (format texte)
- `price_note` - Note sur le prix
- `sku` - Référence/SKU
- `specs` - Spécifications techniques (dictionnaire)
- `date` - Date de publication

### Champs spécifiques aux produits neufs

- `in_stock` - Boolean (true/false)

### Champs spécifiques aux équipements usagés

- `condition` - État (Excellent, Très bon, Bon, etc.)
- `year` - Année de fabrication
- `hours` - Heures d'utilisation

## Notes importantes

- **Ne pas modifier** les fichiers `.md` générés manuellement - ils seront écrasés
- **Modifier uniquement** le fichier `info.yaml` et ajouter les images/PDFs
- Les anciens fichiers `.md` existants dans `content/produits/` et `content/usages/` restent fonctionnels
