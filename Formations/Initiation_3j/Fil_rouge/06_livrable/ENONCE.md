# Étape 06 — Packaging + CLI + livrable

## Contexte

Votre petit frère est convaincu : le programme fonctionne, il est découpé en modules propres. Il reste à en faire un **vrai livrable** : un package installable avec une commande `recettes` qu'il tapera directement dans son terminal, des tests automatiques pour s'assurer que rien ne casse, et un `README.md` pour la postérité.

## Consignes

### 1. `pyproject.toml` complet

1. Compléter le `pyproject.toml` avec :
   - un `[project.scripts]` pour que `recettes` lance `recettes.__main__:main`,
   - une dépendance de développement `[project.optional-dependencies]` → `dev = ["pytest>=8", "ruff>=0.6"]`,
   - la section `[tool.ruff]` et `[tool.pytest.ini_options]`.

### 2. Tests pytest

Écrire au minimum **4 tests** dans `tests/test_recettes.py` :

1. `test_creer_recette_valide` : création d'une recette correcte.
2. `test_creer_recette_nom_vide_leve_exception` : nom vide lève `RecetteInvalide`.
3. `test_sauvegarder_charger_round_trip` : sauvegarder puis recharger donne le même carnet (`tmp_path`).
4. `test_ajouter_recette_incremente` : après `ajouter_recette`, le carnet contient un élément de plus.

### 3. README.md

Écrire un `README.md` à la racine du projet contenant :

- Nom et description du projet.
- Installation (`uv pip install -e .`).
- Utilisation (exemple de commande `recettes`).
- Auteur et licence.

### 4. Build et vérification

```bash
uv venv
uv pip install -e ".[dev]"
recettes --help        # doit fonctionner
pytest -v              # tous les tests passent
ruff check src/ tests/ # pas d'erreur
uv build               # produit un wheel dans dist/
```

## Attendus

Au terme de cette étape, votre petit frère reçoit :

- Un **wheel** installable en une seule commande.
- Une commande `recettes` dans son terminal.
- Un README qui explique tout.

## Critères d'acceptation

- [ ] `pyproject.toml` contient un `[project.scripts]` correct.
- [ ] `tests/test_recettes.py` contient au moins 4 tests.
- [ ] `pytest -v` est vert.
- [ ] `ruff check src/ tests/` ne remonte aucune erreur.
- [ ] `README.md` existe à la racine.
- [ ] `uv build` produit un wheel dans `dist/`.
- [ ] `recettes` est accessible après installation du wheel.

## Temps estimé

2 heures.

## Solution

Voir `solution/`.

## Pièges fréquents

- **Oublier `[tool.hatch.build.targets.wheel] packages`** → le wheel est vide et la commande ne trouve pas le module.
- **Tests qui dépendent de l'ordre** : chaque test doit être **indépendant**. Utiliser `tmp_path` pour l'isolation.
- **`recettes` lance un `ModuleNotFoundError`** → le package n'est pas installé. Relancer `uv pip install -e .`.
- **Confondre `recettes.__main__:main` et `recettes:main`** → le entry point doit pointer vers la **fonction** `main` dans `__main__.py`.
