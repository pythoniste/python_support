# 12_Curses — Interfaces texte plein écran (TUI)

Ce dossier est la **cerise sur le gâteau** du cours. Après avoir vu
comment dialoguer ligne par ligne (`print`, `input`), comment piloter
le terminal via les flux standards et comment réagir aux signaux, on
passe à la dernière étape : prendre le contrôle **complet** du
terminal pour dessiner une interface texte plein écran (en anglais,
*TUI* pour *Text User Interface*).

Le module standard `curses` gère pour nous :

- la bascule du terminal en mode **brut** (touche par touche, sans
  écho) ;
- la lecture des touches spéciales (flèches, fonctions, redimensionnement) ;
- l'écriture à des coordonnées précises de l'écran ;
- la gestion des couleurs et des attributs (gras, inversé...) ;
- la **restauration** du terminal à la sortie, même en cas d'erreur.

C'est ce qui se cache derrière les outils du quotidien comme `htop`,
`vim`, `nano` ou `less`.

## Avertissement important

`curses` fait partie de la bibliothèque standard **sous Linux et macOS
uniquement**. Sous Windows, il faut installer le paquet
`windows-curses` :

```
pip install windows-curses
```

Ce paquet n'est **pas** dans la bibliothèque standard, ce qui sort du
cadre strict du cours. La solution recommandée sous Windows est
d'utiliser **WSL** (*Windows Subsystem for Linux*) et de travailler
dans un vrai terminal Linux.

Autre point crucial : les scripts de ce dossier doivent être lancés
dans un **vrai terminal** (xterm, gnome-terminal, konsole, Terminal.app,
iTerm2, le terminal intégré de VS Code en mode externe, etc.). Les
sorties capturées par certains IDE (PyCharm en mode « run » par
défaut, IDLE, notebooks Jupyter, etc.) n'émulent **pas correctement**
un terminal et `curses` y plantera ou ne s'affichera pas.

## Comment lire ce dossier

Lire les fichiers dans l'ordre numérique. Pour chaque module :

1. Lire le `.md` (1 à 2 pages).
2. Exécuter le `.py` correspondant dans un vrai terminal.
3. Passer au module suivant.

## Pré-requis

- Python 3.10 ou plus récent.
- Avoir parcouru les chapitres 00 à 11 du cours (en particulier les
  flux standards et les signaux).
- Un vrai terminal (pas la console d'un IDE intégrée).
- Sous Windows : WSL, ou bien `pip install windows-curses` (hors stdlib).

## Plan

| Module | Sujet                                          |
|--------|------------------------------------------------|
| 01     | Pourquoi `curses` : mode cooked vs raw         |
| 02     | Premier écran avec `curses.wrapper`            |
| 03     | Couleurs et attributs                          |
| 04     | Redimensionnement et touches spéciales         |

## Validation et mise en pratique

Deux fichiers complètent les quatre modules :

- **`QUIZ.md`** : cinq à six questions courtes pour auto-évaluer la
  compréhension, à utiliser après chaque module ou en fin de parcours.
- **`EXERCICES.md`** : cinq ateliers pratiques de synthèse, à faire
  **après** avoir étudié l'intégralité du dossier.

Les corrigés sont disponibles dans le dossier `CORRIGES/`, à consulter
**après** avoir tenté les ateliers.

À l'issue de ce chapitre, on sait écrire un petit éditeur, un menu
interactif, un tableau de bord ou une horloge plein écran — bref,
toute l'ergonomie d'un outil terminal moderne.
