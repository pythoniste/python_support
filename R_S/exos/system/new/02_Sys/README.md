# 02_Sys — Le module `sys` et le dialogue avec le shell

Ce dossier approfondit ce que le chapitre `00_Concepts` a survolé : les
**arguments de ligne de commande**, les **flux standards** vus depuis
Python, et les **redirections** que le shell applique autour du
programme. Trois fiches courtes, une démo par fiche, des ateliers de
mise en pratique, un quiz.

## Comment lire ce dossier

Lire les fichiers dans l'ordre numérique. Pour chaque module :

1. Lire le `.md` (1 à 2 pages).
2. Exécuter le `.py` correspondant et observer la sortie.
3. Tenter les variantes proposées (avec arguments, avec redirections).
4. Passer au module suivant.

## Pré-requis

- Python 3.10 ou plus récent.
- Avoir lu `00_Concepts/` (notions de stdin/stdout/stderr et de code
  retour déjà rencontrées).
- Un terminal Unix (Bash, Zsh, ou équivalent) pour tester les
  redirections.

## Plan

| Module | Sujet                                          |
|--------|------------------------------------------------|
| 01     | `sys.argv` et `sys.exit`                       |
| 02     | Les flux standards vus depuis Python           |
| 03     | Redirections shell et coopération avec Python  |

## Validation et mise en pratique

Deux fichiers complètent les trois modules :

- **`QUIZ.md`** : cinq questions ouvertes pour auto-évaluer la
  compréhension, à utiliser après chaque module ou en fin de parcours.
- **`EXERCICES.md`** : cinq ateliers pratiques de synthèse, à faire
  **après** avoir étudié l'intégralité du dossier. Stdlib uniquement.

Les corrigés sont disponibles dans le dossier `CORRIGES/`, à consulter
**après** avoir tenté les ateliers.

À l'issue de ces deux étapes, on sait écrire un script Python qui prend
des arguments, lit son entrée, écrit proprement ses sorties et coopère
avec un shell qui le redirige ou le branche dans un *pipe*.
