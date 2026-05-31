# Initiation Python — 5 jours

**Cible :** débutant Python (éventuellement développeur d'un autre langage).
**Objectif :** écrire des scripts Python modernes autonomes, manipuler des données, structurer un projet livrable.
**Fil rouge :** 📚 Gestionnaire de bibliothèque personnelle (voir `Fil_rouge/README.md`).

## Programme jour par jour

### J1 — Prise en main
- **Matin :** Installation, venv (`uv`), REPL, Jupyter/IDE · Variables, types primitifs (`int`, `float`, `str`, `bool`) · Opérateurs et expressions · `print`, `input`
- **Après-midi :** Conditions (`if`/`elif`/`else`, intro `match/case`) · Boucles (`for`, `while`), `break`/`continue`, `else` de boucle
- **Étapes fil rouge :** 01 (matin), 02 (après-midi)

### J2 — Types de données
- **Matin :** Listes et tuples · Dictionnaires et ensembles · Compréhensions de base
- **Après-midi :** Chaînes et f-strings (dont `{x=}`) · `datetime`, `date`, `timedelta`, `zoneinfo` (mention)
- **Étapes fil rouge :** 03 (matin), 04 (après-midi)

### J3 — Fonctions & algorithmique
- **Matin :** Fonctions : paramètres, retours, défauts, `*args`/`**kwargs` · Type hints (introduction) · Portée, closures (intro)
- **Après-midi :** Exceptions (`try`/`except`/`else`/`finally`) · Exceptions personnalisées · Debugging avec `breakpoint()`
- **Étapes fil rouge :** 05 (matin), 06 (après-midi)

### J4 — Modules & fichiers
- **Matin :** Modules standard : `math`, `random`, `statistics`, `pathlib` · Imports, organisation en plusieurs fichiers, `__main__`
- **Après-midi :** Fichiers texte, encodages · CSV (`csv.DictReader`/`DictWriter`) · JSON
- **Étapes fil rouge :** 07 (matin), 08 (après-midi)

### J5 — Qualité, packaging, livrable
- **Matin :** PEP 8, docstrings · `ruff` (format + lint) · `pyproject.toml` (PEP 621) · Structure `src/`
- **Après-midi :** `logging` basique · CLI avec `argparse` + entry point console · Intro `pytest` (3 tests) · Build wheel avec `uv build` · Finalisation fil rouge
- **Étapes fil rouge :** 09 (matin), 10 (après-midi)

## Structure des dossiers jour

Chaque dossier `J?_...` contient les notebooks copiés depuis `Bibliotheque_notebooks/Initiation/` par `tools/build_formation.py`. **Ne pas éditer ces notebooks ici** — éditer dans la bibliothèque source.

## Fil rouge

Le dossier `Fil_rouge/` contient le projet Python classique (10 étapes) avec `ENONCE.md`, `starter/` et `solution/` par étape. Voir `Fil_rouge/README.md`.
