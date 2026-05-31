# bibliotheque

**Gestionnaire de bibliothèque personnelle** — projet livrable du fil rouge
de la formation Python Initiation 5 jours.

Permet de cataloguer des livres (titre, auteur, année, ISBN, date d'ajout),
de rechercher, trier, et sauvegarder/charger en CSV ou JSON.

## Installation

Avec `uv` :

```bash
uv venv
uv pip install -e .
```

Ou depuis le wheel distribué :

```bash
uv pip install dist/bibliotheque-1.0.0-py3-none-any.whl
```

## Utilisation

```bash
bibliotheque --help
bibliotheque                            # menu interactif
bibliotheque --charger livres.json      # charge un catalogue au démarrage
bibliotheque --format csv               # format par défaut pour les sauvegardes
```

## Format des fichiers

**JSON** (liste d'objets) :

```json
[
  {
    "titre": "Le Petit Prince",
    "auteur": "Antoine de Saint-Exupéry",
    "annee": 1943,
    "isbn": "9782070612758",
    "date_ajout": "2026-04-14"
  }
]
```

**CSV** : colonnes `titre,auteur,annee,isbn,date_ajout` avec en-tête.

## Développement

```bash
uv pip install -e ".[dev]"
pytest
ruff check src/ tests/
```

## Auteur et licence

Projet pédagogique — licence MIT.
