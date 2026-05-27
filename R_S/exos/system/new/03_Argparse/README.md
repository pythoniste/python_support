# 03_Argparse — Construire une interface en ligne de commande

Ce dossier introduit `argparse`, le module **standard** de Python pour
analyser les arguments passés en ligne de commande. C'est l'outil qui
transforme une chaîne brute comme `python3 mon_outil.py --verbeux -n 3`
en variables Python prêtes à l'emploi, avec en bonus un `--help`
généré tout seul.

On part de zéro : aucune notion préalable de parsing d'arguments n'est
supposée. Les seuls pré-requis sont les bases de Python et la lecture
du dossier `00_Concepts/` (en particulier `sys.argv` et le code retour).

## Comment lire ce dossier

Lire les fichiers dans l'ordre numérique. Pour chaque fiche :

1. Lire le `.md` (1 à 2 pages).
2. Exécuter le `.py` correspondant avec différents arguments et
   observer la sortie.
3. Lancer aussi le script avec `--help` pour voir l'aide générée.
4. Passer à la fiche suivante.

## Pré-requis

- Python 3.10 ou plus récent.
- Python de base : variables, fonctions, listes, dictionnaires.
- Avoir parcouru `00_Concepts/` (notion de `sys.argv`, stdin/stdout/stderr,
  code retour).
- Un terminal (Bash, Zsh, ou équivalent).

## Plan

| Fiche | Sujet                                                     |
|-------|-----------------------------------------------------------|
| 01    | Premier parser : positionnel, optionnel, `--help`         |
| 02    | Types et validation : `type`, `choices`, `nargs`, defaults |
| 03    | Actions courantes : `store_true`, `count`, `append`       |
| 04    | Sous-commandes : `add_subparsers` et dispatch             |

## Validation et mise en pratique

Trois fichiers complètent les quatre fiches :

- **`QUIZ.md`** : six questions courtes pour auto-évaluer la
  compréhension, à utiliser après chaque fiche ou en fin de parcours.
- **`EXERCICES.md`** : cinq ateliers pratiques de synthèse, à faire
  **après** avoir étudié l'intégralité du dossier.
- **`CORRIGES/`** : un script par atelier, à consulter **après**
  avoir tenté l'exercice.

À l'issue de ce parcours, on sait construire une CLI propre, robuste
et auto-documentée, prête à être réutilisée dans tous les chapitres
suivants.
