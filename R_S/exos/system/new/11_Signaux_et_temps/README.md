# 11_Signaux_et_temps — Horloges, signaux et sortie propre

Ce dossier rassemble trois sujets que tout script « système » finit par
croiser : **mesurer le temps qui passe**, **réagir à un événement
externe** (Ctrl+C, signal d'arrêt), et **garantir une sortie propre**
même quand l'utilisateur interrompt le programme.

Aucun de ces sujets n'est compliqué pris isolément ; l'enjeu est de
savoir lequel utiliser à quel moment. On verra par exemple que
`datetime` n'est *pas* l'outil pour chronométrer une durée, et que
`atexit` n'aide *pas* à survivre à un `kill -9`.

## Comment lire ce dossier

Lire les fichiers dans l'ordre numérique. Pour chaque module :

1. Lire le `.md` (1 à 2 pages).
2. Exécuter le `.py` correspondant et observer la sortie.
3. Passer au module suivant.

## Pré-requis

- Python 3.10 ou plus récent.
- Avoir lu `00_Concepts/` (flux standards, code retour).
- Savoir lancer un script dans un terminal et y taper Ctrl+C.

## Plan

| Module | Sujet                                          |
|--------|------------------------------------------------|
| 01     | Temps et dates : `time`, `datetime`            |
| 02     | Signaux : intercepter Ctrl+C et SIGTERM        |
| 03     | `atexit` : exécuter du code à la sortie        |

## Validation et mise en pratique

Deux fichiers complètent les trois modules :

- **`QUIZ.md`** : six questions courtes pour auto-évaluer la
  compréhension, à utiliser après chaque module ou en fin de parcours.
- **`EXERCICES.md`** : cinq ateliers pratiques de synthèse, à faire
  **après** avoir étudié l'intégralité du dossier. Aucune installation
  tierce n'est requise.

Les corrigés sont disponibles dans le dossier `CORRIGES/`, à consulter
**après** avoir tenté les ateliers.

## Renvois

- `00_Concepts/03_flux_standards.md` : `sys.exit` et code retour.
- `10_Logging/` : pour horodater proprement des événements via
  l'attribut `asctime` plutôt qu'à la main.
- `08_Sous_processus/` : pour envoyer soi-même un signal à un processus
  fils avec `Popen.send_signal(...)`.

À l'issue de ce chapitre, on sait chronométrer une opération avec la
bonne horloge, écrire un script qui s'arrête proprement sur Ctrl+C, et
brancher une fonction de nettoyage à la sortie du programme.
