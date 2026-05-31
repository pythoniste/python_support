# Réservation de salles de réunion

Système de gestion des réservations de salles pour une entreprise.

## Installation

```bash
uv venv
uv pip install -e ".[dev]"
```

## Utilisation

```bash
# Ajouter une salle et un utilisateur
reservation ajouter-salle --code REU-A301 --nom Everest --capacite 10
reservation ajouter-user --email alice@test.fr --nom Alice

# Réserver
reservation reserver --salle REU-A301 --user alice@test.fr --date 2025-06-15T09:00 --duree 60

# Lister les réservations
reservation reservations

# Annuler
reservation annuler --id 1
```

## Architecture

```
src/reservation/
    __init__.py        # version
    __main__.py        # CLI argparse
    modeles.py         # classes OO (Salle, Utilisateur, Reservation)
    schemas.py         # modèles Pydantic (validation)
    protocols.py       # Protocol Reservable
    decorateurs.py     # @log_appel, @timer, @autoriser
    codes.py           # regex de codes de salles
    registry.py        # registre dynamique
    database.py        # persistance sqlite3
    orm.py             # modèles SQLAlchemy
    service.py         # couche service
```

## Tests

```bash
pytest -v --cov=reservation
ruff check .
mypy src/
```

## Build

```bash
uv build
# wheel dans dist/
```

## Auteur

Formation Python.

## Licence

MIT.
