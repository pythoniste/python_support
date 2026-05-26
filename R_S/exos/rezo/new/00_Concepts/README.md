# 00_Concepts — Fondamentaux réseau

Ce dossier ne contient **aucun client ni serveur fonctionnel**. C'est le
vocabulaire et les concepts dont les dossiers `01_` à `13_` se servent ensuite
sans les redéfinir.

## Comment lire ce dossier

Lire les fichiers dans l'ordre numérique. Pour chaque module :

1. Lire le `.md` (1 à 2 pages).
2. Exécuter le `.py` correspondant et observer la sortie.
3. Passer au module suivant.

## Pré-requis

- Python 3.10 ou plus récent.
- Savoir lancer un script en ligne de commande (`python3 fichier.py`).
- **Aucune** connaissance réseau préalable n'est supposée.

## Plan

| Module | Sujet                                |
|--------|--------------------------------------|
| 01     | Adresses : IP, port, hôte, DNS       |
| 02     | Qu'est-ce qu'un socket ?             |
| 03     | TCP vs UDP                           |
| 04     | Cycle de vie client / serveur        |
| 05     | Le problème du *framing*             |
| 06     | Boutisme (endianness)                |
| 07     | Sockets bloquants et non bloquants   |

## Validation et mise en pratique

Deux fichiers complètent les sept modules :

- **`QUIZ.md`** : six questions courtes pour auto-évaluer la
  compréhension, à utiliser après chaque module ou en fin de parcours.
- **`EXERCICES.md`** : huit ateliers pratiques de synthèse, à faire
  **après** avoir étudié l'intégralité du dossier. Aucun serveur tiers
  n'est requis.

À l'issue de ces deux étapes, on peut ouvrir `01_Sockets_bas_niveau/`
et comprendre **chaque ligne** sans surprise.
