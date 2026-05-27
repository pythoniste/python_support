# 10_Logging — Journaliser proprement avec `logging`

Ce dossier remplace l'instinct `print(...)` partout par l'outil standard
de **journalisation** : le module `logging`. On y apprend à distinguer
les niveaux de criticité, à filtrer ce qui s'affiche selon le contexte
(développement ou production) et à diriger les messages vers plusieurs
destinations (console, fichier) avec un format uniforme.

## Comment lire ce dossier

Lire les fichiers dans l'ordre numérique. Pour chaque module :

1. Lire le `.md` (1 à 2 pages).
2. Exécuter le `.py` correspondant et observer la sortie.
3. Passer au module suivant.

## Pré-requis

- Python 3.10 ou plus récent.
- Avoir lu `00_Concepts/` (flux standards, stdout/stderr).
- Savoir manipuler des chemins de fichiers (`04_Pathlib/` recommandé).

## Plan

| Module | Sujet                                          |
|--------|------------------------------------------------|
| 01     | Pourquoi `logging` plutôt que `print`          |
| 02     | Configuration minimale avec `basicConfig`      |
| 03     | Loggers nommés, handlers et formatters         |

## Validation et mise en pratique

Deux fichiers complètent les trois modules :

- **`QUIZ.md`** : six questions courtes pour auto-évaluer la
  compréhension, à utiliser après chaque module ou en fin de parcours.
- **`EXERCICES.md`** : cinq ateliers pratiques de synthèse, à faire
  **après** avoir étudié l'intégralité du dossier. Aucune installation
  tierce n'est requise.

Les corrigés sont disponibles dans le dossier `CORRIGES/`, à consulter
**après** avoir tenté les ateliers.

## Renvois

- `00_Concepts/03_flux_standards.md` : stdout, stderr, redirections.
- `04_Pathlib/` : pour construire proprement les chemins de fichiers de
  journal.
- `11_Signaux_et_temps/` : pour horodater finement les événements.

À l'issue de ce chapitre, on sait remplacer le moindre `print` de
diagnostic par un `logger.debug(...)` ou `logger.info(...)` adapté, et
configurer le niveau global d'une application en une seule ligne.
