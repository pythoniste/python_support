# Étape 07 — Organisation en modules

## Contexte

Votre `main.py` approche les 200 lignes et fait tout : saisie, métier, validation, affichage. Il est temps de **séparer les responsabilités** dans plusieurs fichiers et d'adopter une vraie **structure de projet Python** avec `src/`.

## Consignes

1. Créer l'arborescence suivante :
   ```
   src/
   └── bibliotheque/
       ├── __init__.py
       ├── __main__.py       ← point d'entrée : python -m bibliotheque
       ├── catalogue.py      ← logique métier (creer, ajouter, rechercher, trier)
       ├── exceptions.py     ← LivreInvalide, LivreExistant, CatalogueVide
       └── ui.py             ← affichage et saisie (toutes les fonctions print/input)
   ```
2. Répartir le code de l'étape 06 dans ces modules selon leur responsabilité.
3. Utiliser des **imports absolus** (`from bibliotheque.catalogue import ...`), jamais relatifs à l'intérieur du package.
4. `catalogue.py` **ne doit pas** importer `ui.py`. Dépendance unidirectionnelle : `__main__.py` et `ui.py` peuvent importer `catalogue.py`, jamais l'inverse.
5. Le programme se lance désormais avec :
   ```bash
   cd <projet>
   python -m bibliotheque
   ```
6. Supprimer ou archiver l'ancien `main.py` à la racine.

## Attendus

Le comportement est **identique** à l'étape 06. Ce qui change, c'est la structure du code.

```
<projet>/
├── pyproject.toml           ← minimal pour l'instant (nom du package)
├── src/
│   └── bibliotheque/
│       ├── __init__.py
│       ├── __main__.py
│       ├── catalogue.py
│       ├── exceptions.py
│       └── ui.py
└── tests/
    └── test_etape07.py
```

## Critères d'acceptation

- [ ] Les 5 fichiers existent avec leur responsabilité.
- [ ] `python -m bibliotheque` lance le programme.
- [ ] Aucun import **circulaire**.
- [ ] `catalogue.py` ne contient aucun `print` ni `input`.
- [ ] `pytest tests/test_etape07.py` est vert — il vérifie notamment que `catalogue.py` peut être importé **sans** importer `ui.py`.
- [ ] `ruff check src/` ne remonte aucune erreur.

## Temps estimé

1 h 30.

## Solution

Voir `solution/`.

## Pièges fréquents

- **Oublier l'arborescence `src/`** : les imports ne fonctionnent pas si on fait `python -m bibliotheque` depuis le mauvais dossier. Le `pyproject.toml` à la racine et l'installation en mode éditable (`uv pip install -e .`) règlent tout.
- **`from .catalogue import ...`** : les imports relatifs fonctionnent mais sont déconseillés — toujours absolus à l'intérieur d'un package.
- **Imports circulaires** : si `ui.py` et `catalogue.py` ont besoin l'un de l'autre, c'est que votre découpage est mal fait. `catalogue` doit être **pur métier**, sans affichage.
- **`python bibliotheque/`** au lieu de `python -m bibliotheque` → `ModuleNotFoundError`. Retenir : on utilise `-m` pour exécuter un **module**, pas un fichier.
