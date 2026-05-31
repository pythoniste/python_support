# Fil rouge — 📒 Inventaire de matériel informatique

## Contexte métier

Le service informatique de votre entreprise gère des centaines d'équipements (ordinateurs portables, écrans, serveurs, imprimantes, etc.). Aujourd'hui tout est dans un tableur Excel partagé — source d'erreurs et de conflits. On vous demande un outil en ligne de commande pour **inventorier, rechercher et suivre** le matériel.

Les exigences sont :

- Modéliser les équipements (nom, type, numéro de série, date d'achat, assigné à).
- Valider les données avec des types stricts et Pydantic.
- Persister les données en base SQLite.
- Tester le tout avec pytest.
- Livrer sous forme de package installable.

Ce projet vous accompagne sur les 3 jours de la formation intermédiaire. À chaque demi-journée, vous enrichissez le programme.

## Progression

| # | Moment | Étape | Livrable de l'étape |
|---|---|---|---|
| 01 | J1 matin | Modèles OO | Classes `Equipement`, `Utilisateur`, héritage (`Portable`, `Ecran`, `Serveur`) |
| 02 | J1 après-midi | Validation Pydantic | `BaseModel`, validators, sérialisation JSON |
| 03 | J2 matin | Décorateurs | `@log_action`, `@timer`, context managers |
| 04 | J2 après-midi | Persistance SQL | `sqlite3`, schéma, CRUD |
| 05 | J3 matin | Tests pytest | Fixtures, parametrize, mocks |
| 06 | J3 après-midi | Packaging | `pyproject.toml`, CLI, wheel, README |

## Structure des étapes

Chaque dossier `NN_titre/` contient :

- **`ENONCE.md`** : les consignes et les attendus.
- **`starter/`** : un projet de départ à compléter.
- **`solution/`** : la solution **cumulative** et **autonome**.

## Livrable final (fin J3)

```bash
cd 06_packaging/solution
uv venv
uv pip install -e ".[dev]"
inventaire --help
pytest -v
```

## Comment utiliser ce fil rouge ?

1. Lire `ENONCE.md`.
2. Copier `starter/` dans un dossier de travail.
3. Implémenter, tester, comparer.
4. Passer à l'étape suivante.

Bon courage !
