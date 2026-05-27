# 07_Compression — Compresser et archiver des fichiers

La compression réduit la taille des données sur disque ou sur le
réseau. L'archivage rassemble plusieurs fichiers dans un seul. Les
deux notions sont souvent confondues parce que les outils du quotidien
(`.zip`, `.tar.gz`) font les deux d'un coup — mais en Python, ce sont
deux briques distinctes, livrées dans la bibliothèque standard.

## Fichier compressé seul, ou archive ?

C'est la distinction centrale du chapitre.

| Cas                 | Modules concernés         | Extension typique          |
|---------------------|---------------------------|----------------------------|
| Un seul fichier     | `gzip`, `bz2`, `lzma`     | `.gz`, `.bz2`, `.xz`       |
| Plusieurs fichiers  | `zipfile`, `tarfile`      | `.zip`, `.tar`, `.tar.gz`  |

- Avec `gzip`, `bz2` ou `lzma`, on compresse **un fichier** (ou un
  flux d'octets) et on obtient **un fichier** compressé. Aucune
  notion d'arborescence, aucun nom de fichier interne.
- Avec `zipfile` ou `tarfile`, on regroupe **plusieurs fichiers**
  (avec leur arborescence) dans une **archive** unique, qui peut
  elle-même être compressée.

Le format `.tar.gz` (très courant sous Unix) combine les deux :
`tar` produit une archive non compressée, puis `gzip` la compresse.
Le module `tarfile` fait ça en un seul appel.

## Comment lire ce dossier

Lire les fichiers dans l'ordre numérique. Pour chaque fiche :

1. Lire le `.md`.
2. Exécuter le `.py` correspondant et observer la sortie.
3. Passer à la suivante.

## Pré-requis

- Python 3.10 ou plus récent.
- Avoir suivi les chapitres `04_Pathlib`, `05_Fichiers` et
  `06_OS_et_Shutil` (parcours de dossiers, lecture binaire).

## Plan

| Fiche | Sujet                                                        |
|-------|--------------------------------------------------------------|
| 01    | Compresser un fichier seul : `gzip`, `bz2`, `lzma`           |
| 02    | Archives `.zip` avec `zipfile`                               |
| 03    | Archives `.tar` (et `.tar.gz`, `.tar.bz2`, `.tar.xz`)        |

## Validation et mise en pratique

- **`EXERCICES.md`** : six ateliers pratiques (★ à ★★★), à faire
  après avoir lu les trois fiches.
- **`QUIZ.md`** : six questions ouvertes pour auto-évaluer la
  compréhension.

Les corrigés des ateliers se trouvent dans `CORRIGES/`, à consulter
**après** avoir tenté chaque atelier.

## Renvois

- Chapitre `05_Fichiers` : lecture/écriture binaire (`"rb"`, `"wb"`).
- Chapitre `04_Pathlib` : `Path.glob`, `Path.rglob` pour parcourir
  un dossier avant de l'archiver.
- Chapitre `06_OS_et_Shutil` : `shutil.make_archive` est une
  alternative plus haut niveau (non détaillée ici).
