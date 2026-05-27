# 01_Print_et_Input — Afficher et lire au clavier

Ce dossier rassemble les **briques d'interaction de base** entre un
programme Python et son utilisateur : afficher du texte à l'écran,
le formater proprement, et lire ce que la personne tape au clavier.

Tout le reste du cours s'appuie sur ces trois primitives sans les
redéfinir. Avant d'aller plus loin, on les maîtrise au point de
pouvoir :

- choisir le séparateur, la fin de ligne et la destination d'un `print` ;
- formater un nombre flottant avec une précision donnée et un alignement ;
- lire une valeur saisie, la convertir, et redemander en cas d'erreur.

## Comment lire ce dossier

Lire les fichiers dans l'ordre numérique. Pour chaque module :

1. Lire le `.md` (1 à 2 pages).
2. Exécuter le `.py` correspondant et observer la sortie.
3. Passer au module suivant.

## Pré-requis

- Python 3.10 ou plus récent.
- Python de base : variables, conditions, boucles, fonctions, exceptions.
- Avoir parcouru `00_Concepts/` (flux standards, code retour).

## Plan

| Module | Sujet                                          |
|--------|------------------------------------------------|
| 01     | `print()` : signature complète et redirection  |
| 02     | f-strings : interpolation et format spec       |
| 03     | `input()` : lire, convertir, valider, masquer  |

## Validation et mise en pratique

Deux fichiers complètent les trois modules :

- **`QUIZ.md`** : six questions courtes pour auto-évaluer la
  compréhension, à utiliser après chaque module ou en fin de parcours.
- **`EXERCICES.md`** : six ateliers pratiques de synthèse, à faire
  **après** avoir étudié l'intégralité du dossier. Aucune installation
  tierce n'est requise.

Les corrigés sont disponibles dans le dossier `CORRIGES/`, à consulter
**après** avoir tenté les ateliers.

À l'issue de ces deux étapes, on est outillé pour écrire des petits
programmes qui dialoguent avec l'utilisateur, et pour formater
proprement n'importe quelle sortie texte.
