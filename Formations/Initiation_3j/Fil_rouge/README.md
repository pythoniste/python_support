# Fil rouge — 📝 Carnet de recettes

## Contexte métier

Votre petit frère se met à la cuisine et veut garder ses recettes quelque part. Il aimerait un petit programme Python où il peut **saisir, lister, sauvegarder et rechercher** des recettes — chacune a un nom, une liste d'ingrédients et un temps de préparation.

Sur les 3 jours de la formation, vous allez construire ce carnet de recettes, demi-journée après demi-journée. À la fin du J3, vous aurez un **package Python installable** avec une commande `recettes`.

## Progression

| # | Moment | Étape | Livrable de l'étape |
|---|---|---|---|
| 01 | J1 matin | Premier script | Un script `main.py` qui saisit et affiche une recette |
| 02 | J1 après-midi | Menu et liste en mémoire | Ajouter, lister, quitter dans une boucle |
| 03 | J2 matin | Fonctions et gestion d'erreurs | Découpe en fonctions, exception `RecetteInvalide` |
| 04 | J2 après-midi | Persistance JSON | Sauvegarder et charger le carnet |
| 05 | J3 matin | Découpe en modules | `src/recettes/` avec `carnet.py`, `ui.py`, `__main__.py` |
| 06 | J3 après-midi | Packaging + CLI + livrable | `pyproject.toml`, entry point `recettes`, tests, wheel |

## Structure des étapes

Chaque dossier `NN_titre/` contient :

- **`ENONCE.md`** : les consignes et les attendus de l'étape.
- **`starter/`** : un projet de départ à compléter.
- **`solution/`** : la solution **cumulative** et **autonome**.

## Livrable final (fin J3)

```bash
cd 06_packaging_et_livrable/solution
uv venv
uv pip install -e .
recettes --help
pytest
```

## Comment utiliser ce fil rouge ?

1. Lire `ENONCE.md`.
2. Copier `starter/` dans un dossier de travail.
3. Implémenter, tester, comparer.
4. Passer à l'étape suivante en repartant de votre code (ou de la `solution/` précédente).

Bon courage !
