# 04_Pathlib — Manipuler les chemins de fichiers

Ce dossier introduit `pathlib`, le module **moderne** de la bibliothèque
standard pour manipuler des chemins de fichiers. C'est la base de tout
script qui touche au disque : ouvrir, lister, filtrer, inspecter.

L'ancienne approche reposait sur `os.path` et beaucoup de chaînes de
caractères concaténées à la main. La nouvelle, fondée sur la classe
`Path`, est plus lisible, multiplateforme, et expose des méthodes
**orientées objet** sur l'objet chemin lui-même.

## Comment lire ce dossier

Lire les fichiers dans l'ordre numérique. Pour chaque fiche :

1. Lire le `.md` (1 à 2 pages).
2. Exécuter le `.py` correspondant et observer la sortie.
3. Passer à la fiche suivante.

## Pré-requis

- Python 3.10 ou plus récent.
- Avoir parcouru `00_Concepts/` (script, REPL, flux standards).
- Un terminal (Bash, Zsh, ou équivalent).
- **Aucune** connaissance préalable de `os.path` n'est nécessaire.

## Plan

| Fiche | Sujet                                            |
|-------|--------------------------------------------------|
| 01    | `Path` de base : construction, assemblage, attributs |
| 02    | Inspecter un chemin : existence, type, métadonnées |
| 03    | Parcourir et filtrer : `iterdir`, `glob`, `rglob`    |

## Validation et mise en pratique

Deux fichiers complètent les trois fiches :

- **`QUIZ.md`** : six questions courtes pour auto-évaluer la
  compréhension, à utiliser après chaque fiche ou en fin de parcours.
- **`EXERCICES.md`** : six ateliers pratiques de synthèse, à faire
  **après** avoir étudié l'intégralité du dossier. Tout se fait avec
  la bibliothèque standard.

Les corrigés sont disponibles dans le dossier `CORRIGES/`, à consulter
**après** avoir tenté chaque atelier.

À l'issue de ces deux étapes, on peut ouvrir les chapitres suivants
(lecture/écriture de fichiers, processus, archives) et manipuler des
chemins **sans hésitation**.
