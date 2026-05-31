# Carnet de recettes

Petit programme Python pour saisir, lister, sauvegarder et rechercher des recettes.

## Installation

```bash
uv venv
uv pip install -e ".[dev]"
```

## Utilisation

```bash
recettes                    # lance le menu interactif
recettes --charger carnet.json  # charge un carnet existant
recettes --verbose          # active les logs de debug
recettes --help             # affiche l'aide
```

## Tests

```bash
pytest -v
ruff check src/ tests/
```

## Build

```bash
uv build
# le wheel est dans dist/
```

## Auteur

Formation Python.

## Licence

MIT.
