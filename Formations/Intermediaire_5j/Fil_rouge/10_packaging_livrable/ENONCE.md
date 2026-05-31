# Étape 10 — Packaging et livrable

## Contexte

Le code est complet, testé, typé. C'est le dernier sprint : on ajoute une **CLI** avec `argparse`, on finalise le `pyproject.toml`, on construit un **wheel** distribuable et on rédige le **README**.

## Consignes

### 1. CLI avec argparse

Créer `__main__.py` avec des sous-commandes :
- `reservation salles` : liste les salles.
- `reservation reserver --salle REU-A301 --user alice@test.fr --date 2025-06-15T09:00 --duree 60`.
- `reservation reservations` : liste les réservations.
- `reservation annuler --id 1`.

### 2. pyproject.toml complet

- `[project.scripts]` : `reservation = "reservation.__main__:main"`.
- `[project.optional-dependencies]` : dev = `["pytest>=8", "pytest-cov>=5", "ruff>=0.6", "mypy>=1.11"]`.
- `[tool.ruff]`, `[tool.mypy]`.

### 3. README.md

- Installation, utilisation, architecture, tests, licence.

### 4. Vérification finale

```bash
uv venv && uv pip install -e ".[dev]"
reservation --help
pytest -v --cov=reservation
ruff check .
mypy src/
uv build
```

## Critères d'acceptation

- [ ] `reservation --help` fonctionne.
- [ ] Les 4 sous-commandes fonctionnent.
- [ ] `pytest -v` est vert.
- [ ] `ruff check .` ne remonte aucune erreur.
- [ ] `README.md` existe.
- [ ] `uv build` produit un wheel.

## Temps estimé

2 heures.

## Solution

Voir `solution/`.

## Pièges fréquents

- **`argparse` sub-commands** : utiliser `add_subparsers` avec `set_defaults(func=...)`.
- **Oublier le `[project.scripts]`** dans `pyproject.toml` → la commande `reservation` n'existe pas après installation.
- **`uv build` échoue** → vérifier que `packages = ["src/reservation"]` est correct.
