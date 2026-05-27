# Programmation système avec Python

Support de cours pour la partie **système** du module « Système & Réseau ».
Public visé : débutants en Python ayant déjà vu les bases du langage
(variables, conditions, boucles, fonctions, exceptions). Aucune
expérience préalable de la programmation système n'est supposée.

## Comment utiliser ce cours

Chaque chapitre est un dossier numéroté. Dans chaque dossier :

1. Lire le `README.md` du chapitre (1 page d'introduction).
2. Lire les fiches `01_xxx.md`, `02_xxx.md`, ... dans l'ordre.
3. Exécuter le script `NN_demo_xxx.py` correspondant à chaque fiche.
4. Faire les ateliers de `EXERCICES.md`.
5. Vérifier ses acquis avec `QUIZ.md`.

Les corrigés des ateliers se trouvent dans `CORRIGES/` (non versionné).

## Plan

| #   | Chapitre                 | Sujet                                           |
|-----|--------------------------|-------------------------------------------------|
| 00  | `00_Concepts`            | Programme, script, REPL, flux standards         |
| 01  | `01_Print_et_Input`      | Dialoguer avec l'utilisateur                    |
| 02  | `02_Sys`                 | Le module `sys` et les flux                     |
| 03  | `03_Argparse`            | Construire une CLI propre                       |
| 04  | `04_Pathlib`             | Manipuler les chemins                           |
| 05  | `05_Fichiers`            | Lire et écrire des fichiers                     |
| 06  | `06_OS_et_Shutil`        | Copier, déplacer, parcourir                     |
| 07  | `07_Compression`         | Archives : gzip, zip, tar                       |
| 08  | `08_Sous_processus`      | Lancer d'autres programmes                      |
| 09  | `09_Environnement`       | Variables d'env et fichiers de configuration    |
| 10  | `10_Logging`             | Tracer une application                          |
| 11  | `11_Signaux_et_temps`    | Réagir au système, mesurer du temps             |
| 12  | `12_Curses`              | Interfaces texte plein écran (TUI)              |

## Pré-requis techniques

- Python **3.11** ou plus récent (pour `tomllib`, `match/case`).
- Un terminal Linux/macOS (Windows : utiliser WSL pour le chapitre 12).
- Aucune dépendance externe : tout est dans la bibliothèque standard.

## Conventions

- Les blocs `$ python3 ...` indiquent une commande à taper dans le shell.
- Les blocs `>>> ...` indiquent une session interactive Python (REPL).
- Le bloc « À retenir » à la fin de chaque fiche résume l'essentiel.
