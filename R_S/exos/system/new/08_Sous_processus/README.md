# 08_Sous_processus — Lancer un programme externe depuis Python

Ce chapitre montre comment exécuter une **commande externe** (un autre
programme, typiquement un utilitaire Unix comme `ls`, `date`, `wc`...)
depuis un script Python et récupérer ce qu'elle a produit : son texte
de sortie, son texte d'erreur, son code retour.

Tout passe par le module `subprocess` de la bibliothèque standard. On
verra surtout `subprocess.run`, la fonction recommandée depuis Python
3.5 et qui couvre l'immense majorité des cas.

## Comment lire ce dossier

Lire les fichiers dans l'ordre numérique. Pour chaque module :

1. Lire le `.md` (1 à 2 pages).
2. Exécuter le `.py` correspondant et observer la sortie.
3. Passer au module suivant.

## Pré-requis

- Python 3.10 ou plus récent.
- Avoir lu `00_Concepts/03_flux_standards.md` : on y a vu stdin,
  stdout, stderr et le code retour. Ce chapitre s'appuie dessus de
  bout en bout.
- Un système Unix (Linux, macOS) avec les utilitaires de base : `ls`,
  `echo`, `cat`, `wc`, `date`, `sleep`.

## Plan

| Module | Sujet                                          |
|--------|------------------------------------------------|
| 01     | `subprocess.run` : la fonction recommandée     |
| 02     | Code retour et erreurs                         |
| 03     | Pipes et `Popen` (survol)                      |

## Validation et mise en pratique

Deux fichiers complètent les trois modules :

- **`QUIZ.md`** : six questions courtes pour auto-évaluer la
  compréhension.
- **`EXERCICES.md`** : cinq ateliers pratiques de synthèse, à faire
  **après** avoir étudié l'intégralité du dossier.

Les corrigés sont disponibles dans `CORRIGES/`, à consulter **après**
avoir tenté chaque atelier.

## Renvois

- Pour le rappel sur stdin/stdout/stderr et le code retour, voir
  `00_Concepts/03_flux_standards.md`.
- Le chapitre `09_Environnement` montrera comment passer des variables
  d'environnement à un sous-processus.

## Avertissement de sécurité

`subprocess` permet aussi de passer la commande à un **shell** via
`shell=True`. Tout ce chapitre l'évite : c'est dangereux dès qu'une
partie de la commande vient de l'utilisateur (risque **d'injection de
commande**). On le redit à chaque fiche : la valeur sûre par défaut
est `shell=False` et une liste d'arguments.
