# Étape 05 — Découpe en modules

## Contexte

Le `main.py` dépasse 100 lignes. On le découpe en plusieurs modules avec une arborescence `src/recettes/`.

## Consignes

1. Créer l'arborescence :
   ```
   src/
   └── recettes/
       ├── __init__.py
       ├── __main__.py
       ├── carnet.py       ← métier + persistance
       └── ui.py           ← affichage et saisie
   ```
2. `carnet.py` : `creer_recette`, `ajouter_recette`, `sauvegarder`, `charger`, `RecetteInvalide`. Aucun `print`/`input`.
3. `ui.py` : `afficher_menu`, `saisir_recette`, `formater_recette`, `afficher_carnet`.
4. `__main__.py` : fonction `main()` avec la boucle principale.
5. Imports **absolus** : `from recettes.carnet import ...`.
6. Le programme se lance avec `python -m recettes`.
7. Créer un `pyproject.toml` minimal pour que `src/recettes/` soit installable en mode éditable.

## Attendus

Le comportement est **identique** à l'étape 04.

## Critères d'acceptation

- [ ] Les 4 fichiers existent avec les bonnes responsabilités.
- [ ] `python -m recettes` fonctionne.
- [ ] `carnet.py` ne contient ni `print` ni `input`.
- [ ] Pas d'import circulaire.

## Temps estimé

1 h 30.

## Solution

Voir `solution/`.

## Pièges fréquents

- **`python recettes/`** au lieu de `python -m recettes` → `ModuleNotFoundError`.
- **Imports relatifs `from .carnet import ...`** fonctionnent mais sont déconseillés — préférez les imports absolus.
- **Oublier `src/` layout** → les imports ne marchent que si vous êtes dans le bon dossier ou que le package est installé.
