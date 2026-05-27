# 13_Boite_a_outils — Cinq modules utilitaires de la stdlib

Ce dossier rassemble cinq petits modules de la bibliothèque standard
qui n'avaient pas leur chapitre dédié mais qu'**on retrouve partout** :
créer des fichiers temporaires, savoir sur quelle machine on tourne,
calculer une empreinte, générer un secret, encoder en base64. Aucun
n'est compliqué, mais les ignorer mène vite à du code maladroit ou
dangereux (jamais de `random` pour un mot de passe, jamais de `mkdtemp`
sans nettoyage…).

On suppose ici les chapitres précédents acquis : ouverture de fichiers
(05), `pathlib` (04), `os`/`shutil` (06). Ce chapitre n'apporte pas de
nouveau concept système, juste cinq fiches autonomes qui mobilisent les
bons réflexes au bon moment.

## Comment lire ce dossier

Lire les fichiers dans l'ordre numérique. Pour chaque module :

1. Lire le `.md` (1 à 2 pages).
2. Exécuter le `.py` correspondant et observer la sortie.
3. Passer au module suivant.

## Pré-requis

- Python 3.10 ou plus récent.
- Avoir lu les chapitres `04_Pathlib`, `05_Fichiers` et `06_OS_et_Shutil`.
- Savoir lancer un script avec `python3 fichier.py`.

## Plan

| Module | Sujet                                                       |
|--------|-------------------------------------------------------------|
| 01     | `tempfile` — fichiers et dossiers temporaires               |
| 02     | `platform` — connaître la machine et l'OS                   |
| 03     | `hashlib` — empreintes cryptographiques                     |
| 04     | `secrets` et `hmac` — générer et signer                     |
| 05     | `base64` — encoder des octets en ASCII transportable        |

## Validation et mise en pratique

Deux fichiers complètent les cinq modules :

- **`QUIZ.md`** : six questions courtes pour auto-évaluer la
  compréhension, à utiliser après chaque module ou en fin de parcours.
- **`EXERCICES.md`** : cinq ateliers pratiques de synthèse, à faire
  **après** avoir étudié l'intégralité du dossier. Aucune installation
  tierce n'est requise ; tous les corrigés créent eux-mêmes leurs
  fichiers de test pour rester exécutables tels quels.

Les corrigés sont disponibles dans le dossier `CORRIGES/`, à consulter
**après** avoir tenté les ateliers.

## Renvois

- Chapitre **05_Fichiers** : on lit et on écrit ici beaucoup de petits
  fichiers, toujours avec `with open(...)`.
- Chapitre **06_OS_et_Shutil** : compléments pour copier ou déplacer
  les fichiers temporaires une fois prêts.
- Les fiches 03 et 04 préparent le chapitre **réseau / TLS** : signer
  un message, vérifier un token, comparer en temps constant.
