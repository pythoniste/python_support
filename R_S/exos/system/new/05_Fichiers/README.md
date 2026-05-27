# 05_Fichiers — Ouvrir, lire, écrire

Ce dossier présente la **brique de base** de toute interaction avec le
disque en Python : la fonction `open()` et le bloc `with`. Une fois ces
trois fiches lues, on saura lire un fichier texte ligne à ligne, écrire
sans tout perdre, et faire la différence entre **texte** et **octets**.

On suppose ici que les chemins ont déjà été construits proprement avec
`pathlib` (chapitre 04). Ce chapitre se concentre sur le **contenu** des
fichiers, pas sur leur localisation.

## Comment lire ce dossier

Lire les fichiers dans l'ordre numérique. Pour chaque module :

1. Lire le `.md` (1 à 2 pages).
2. Exécuter le `.py` correspondant et observer la sortie.
3. Passer au module suivant.

## Pré-requis

- Python 3.10 ou plus récent.
- Avoir lu les chapitres `00_Concepts` (encodage, flux standards) et
  `04_Pathlib` (construction de chemins).
- Savoir lancer un script avec `python3 fichier.py`.

## Plan

| Module | Sujet                                    |
|--------|------------------------------------------|
| 01     | Ouvrir et lire un fichier texte          |
| 02     | Écrire dans un fichier                   |
| 03     | Texte ou binaire : choisir le bon mode   |

## Validation et mise en pratique

Deux fichiers complètent les trois modules :

- **`QUIZ.md`** : six questions courtes pour auto-évaluer la
  compréhension, à utiliser après chaque module ou en fin de parcours.
- **`EXERCICES.md`** : six ateliers pratiques de synthèse, à faire
  **après** avoir étudié l'intégralité du dossier. Aucune installation
  tierce n'est requise ; tous les corrigés créent eux-mêmes leurs
  fichiers de test pour rester exécutables tels quels.

Les corrigés sont disponibles dans le dossier `CORRIGES/`, à consulter
**après** avoir tenté les ateliers.

## Renvois

- Chapitre **04_Pathlib** : construire un `Path` portable avant
  d'appeler `open()`.
- Chapitre **06_OS_et_Shutil** : copier, déplacer, supprimer des
  fichiers entiers sans en lire le contenu.
- Chapitre **07_Compression** : lire et écrire des fichiers `.gz`,
  `.zip` ou `.tar` — on retrouvera exactement les mêmes modes
  (`"r"`, `"rb"`, `"w"`, `"wb"`).
