# Fil rouge — 🏢 Réservation de salles de réunion

## Contexte métier

Votre entreprise dispose de plusieurs salles de réunion et de formation. Jusqu'ici, les réservations se font sur un tableau blanc dans le couloir — ce qui génère des conflits, des oublis et des frustrations. La direction vous demande un outil en ligne de commande pour **gérer les salles, les utilisateurs et les réservations**.

Les exigences sont :

- Modéliser les salles (nom, capacité, équipements) et les utilisateurs.
- Gérer les réservations (créer, annuler, lister, détecter les conflits).
- Valider les données avec des types stricts et des validateurs.
- Persister les données en base SQL.
- Livrer le tout sous forme de package installable avec tests.

Ce projet vous accompagne sur les 5 jours de la formation intermédiaire. À chaque demi-journée, vous enrichissez le programme d'une nouvelle capacité. À la fin du J5, vous disposez d'un **package Python distribuable** avec ORM, tests, CLI et documentation.

## Structure des étapes

Chaque dossier `NN_titre/` contient :

- **`ENONCE.md`** : les consignes, attendus et critères d'acceptation de l'étape.
- **`starter/`** : un projet de départ avec `pyproject.toml`, un squelette de `src/reservation/`, et des tests pytest déjà écrits. Vous implémentez le code manquant jusqu'à ce que les tests passent.
- **`solution/`** : une proposition de solution **complète et cumulative**. Elle contient le projet entier à ce stade, pas seulement un diff. À consulter **après** tentative personnelle.

## Progression

| # | Moment | Étape | Livrable de l'étape |
|---|---|---|---|
| 01 | J1 matin | Modèles OO | Classes `Salle`, `Utilisateur`, `Reservation` avec `__init__`, `__str__`, `__repr__` |
| 02 | J1 après-midi | Hiérarchie de salles | `SalleReunion`, `SalleFormation`, héritage, surcharge d'opérateurs |
| 03 | J2 matin | Typage complet | Type hints modernes, `Protocol`, `mypy --strict` vert |
| 04 | J2 après-midi | Validation Pydantic | `BaseModel`, validators, sérialisation JSON |
| 05 | J3 matin | Décorateurs métier | `@log_appel`, `@timer`, `@autoriser` |
| 06 | J3 après-midi | Registry et regex | Patterns de codes de salles, registre dynamique |
| 07 | J4 matin | Persistance SQL | `sqlite3`, schéma, CRUD, requêtes paramétrées |
| 08 | J4 après-midi | SQLAlchemy ORM | Migration vers SQLAlchemy 2, modèles déclaratifs |
| 09 | J5 matin | Tests pytest | Fixtures, parametrize, mocks, couverture |
| 10 | J5 après-midi | Packaging et livrable | `pyproject.toml`, CLI, wheel, README |

## Livrable final (fin J5)

À la fin de l'étape 10, vous devez pouvoir exécuter :

```bash
cd 10_packaging_livrable/solution
uv venv
uv pip install -e ".[dev]"
reservation --help    # lance votre CLI
pytest -v             # tous les tests passent
ruff check .          # aucune erreur de lint
mypy src/             # aucune erreur de typage
```

## Comment utiliser ce fil rouge ?

1. **Lire l'`ENONCE.md`** de l'étape en cours.
2. **Copier le `starter/`** ailleurs (par exemple dans un dossier `mon_travail/` à côté). C'est votre espace de travail.
3. **Implémenter** le code manquant. Lancer `pytest` régulièrement pour vérifier votre progression.
4. **Comparer avec `solution/`** une fois terminé (ou après 45 minutes de recherche infructueuse — pas avant !).
5. **Passer à l'étape suivante** en repartant de votre code si tout est vert, ou de la `solution/` précédente si vous avez pris du retard.

Bon courage !
