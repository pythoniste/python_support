# 09_Environnement — Variables d'environnement et fichiers de configuration

Ce dossier explique comment un programme Python lit sa **configuration**.
Trois sources reviennent en pratique : les **variables d'environnement**
exposées par le shell, les fichiers **INI** lus avec `configparser`, et
les fichiers **TOML** lus avec `tomllib` (utilisés par
`pyproject.toml`). À la fin du dossier, on sait combiner ces sources
dans un ordre de priorité raisonnable.

## Comment lire ce dossier

Lire les fichiers dans l'ordre numérique. Pour chaque module :

1. Lire le `.md` (1 à 2 pages).
2. Exécuter le `.py` correspondant et observer la sortie.
3. Passer au module suivant.

## Pré-requis

- Python 3.11 ou plus récent (le module `tomllib` est arrivé en 3.11).
- Avoir lu le dossier `00_Concepts` (flux standards, `sys.argv`).
- Un terminal pour définir des variables d'environnement.
- **Aucune** dépendance tierce : tout est dans la bibliothèque standard.

## Plan

| Module | Sujet                                          |
|--------|------------------------------------------------|
| 01     | Variables d'environnement avec `os.environ`    |
| 02     | Fichiers INI avec `configparser`               |
| 03     | Fichiers TOML avec `tomllib` (+ ordre des sources) |

## Validation et mise en pratique

Deux fichiers complètent les trois modules :

- **`QUIZ.md`** : six questions courtes pour auto-évaluer la
  compréhension, à utiliser après chaque module ou en fin de parcours.
- **`EXERCICES.md`** : cinq ateliers pratiques de synthèse, à faire
  **après** avoir étudié l'intégralité du dossier.

Les corrigés sont disponibles dans le dossier `CORRIGES/`, à consulter
**après** avoir tenté les ateliers.

À l'issue de ces deux étapes, on est capable d'écrire un script qui
combine plusieurs sources de configuration sans surprise.
