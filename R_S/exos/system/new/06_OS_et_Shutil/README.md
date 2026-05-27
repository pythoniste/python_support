# 06_OS_et_Shutil — Manipuler l'arborescence

Le chapitre précédent (`05_Fichiers`) a couvert la lecture et l'écriture
**du contenu** d'un fichier. Ici, on s'intéresse à l'arborescence
elle-même : **parcourir** un dossier, **copier**, **déplacer**,
**renommer**, **supprimer** des fichiers et des dossiers, et ajuster
leurs **droits**.

Deux modules de la bibliothèque standard portent ces opérations :

- **`os`** : interface bas niveau, proche du système.
- **`shutil`** : utilitaires de haut niveau (recopie récursive, etc.).

On utilise aussi **`pathlib.Path`** (vu au chapitre 04) pour la
plupart des chemins. `os` et `pathlib` se complètent : `pathlib`
est plus lisible pour les opérations courantes, `os` reste
indispensable pour quelques cas (parcours `os.walk`, droits `chmod`).

## Avertissement

Plusieurs fonctions de ce chapitre sont **destructives** et
**irréversibles** :

- `shutil.rmtree(dossier)` supprime un dossier **et tout son contenu**,
  récursivement, sans confirmation et sans corbeille.
- `os.remove(fichier)` / `Path.unlink()` supprime un fichier
  immédiatement.
- `shutil.move(...)` peut **écraser** une destination existante.

Sur un système Unix, ces fonctions ne déplacent **rien** vers la
corbeille graphique : les données sont perdues. Toujours tester les
scripts dans un dossier jetable (idéalement un `tempfile.TemporaryDirectory()`)
avant de les lâcher sur des données réelles.

## Comment lire ce dossier

Lire les fiches dans l'ordre numérique. Pour chaque fiche :

1. Lire le `.md` (1 à 3 pages).
2. Exécuter le `.py` correspondant et observer la sortie. Tous les
   scripts de démo travaillent dans un dossier temporaire qu'ils
   créent et nettoient eux-mêmes.
3. Passer à la fiche suivante.

## Pré-requis

- Python 3.10 ou plus récent.
- Avoir lu les chapitres `04_Pathlib` et `05_Fichiers`.
- Un terminal pour lancer les scripts.

## Plan

| Fiche | Sujet                                         |
|-------|-----------------------------------------------|
| 01    | Parcourir une arborescence                    |
| 02    | Copier et déplacer                            |
| 03    | Renommer, supprimer, ajuster les droits       |

## Validation et mise en pratique

Deux fichiers complètent les trois fiches :

- **`QUIZ.md`** : six questions courtes pour auto-évaluer la
  compréhension.
- **`EXERCICES.md`** : cinq ateliers pratiques de synthèse, à faire
  **après** avoir étudié l'intégralité du dossier.

Les corrigés sont disponibles dans le dossier `CORRIGES/`, à consulter
**après** avoir tenté les ateliers. Tous les corrigés des opérations
destructives travaillent dans un `tempfile.TemporaryDirectory()`
peuplé par le script lui-même — **jamais** sur les données de
l'utilisateur.
