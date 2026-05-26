# 02_Framing — Résoudre le découpage des messages

Le dossier 01 a démontré (atelier 4) que `recv(N)` ne renvoie pas
« un message » mais « ce qui est arrivé jusqu'à présent, jusqu'à N
octets ». Pour échanger des messages structurés, il faut un mécanisme
**explicite** pour marquer leurs frontières — c'est ce qu'on appelle
le *framing*.

Ce dossier présente les **trois stratégies classiques** et les met
en œuvre dans trois paires client/serveur.

## Plan

| Fichier(s)                                      | Stratégie                                  |
|-------------------------------------------------|--------------------------------------------|
| `aux_framing.py`                                | Helpers utilisés partout                   |
| `01_delimiteur_srv.py` + `02_delimiteur_clt.py` | Délimiteur (`\n`), implémenté à la main    |
| `03_prefixe_srv.py` + `04_prefixe_clt.py`       | Préfixe de longueur (4 octets big-endian)  |
| `05_makefile_srv.py` + `06_makefile_clt.py`     | `socket.makefile()` — abstraction stdlib   |

## Comment exécuter

Comme au dossier 01, deux terminaux. Démarrer le serveur d'une paire,
puis le client correspondant :

```
# Paire 1 — délimiteur manuel
python3 01_delimiteur_srv.py    # terminal 1
python3 02_delimiteur_clt.py    # terminal 2

# Paire 2 — préfixe de longueur
python3 03_prefixe_srv.py
python3 04_prefixe_clt.py

# Paire 3 — makefile
python3 05_makefile_srv.py
python3 06_makefile_clt.py
```

Toutes les paires utilisent le port `8808`. Un seul serveur à la
fois.

## Ce qui est démontré

- **Délimiteur** (paire 1). On choisit un octet (typiquement `\n`)
  qui ne peut pas apparaître dans le contenu, et on lit jusqu'à le
  rencontrer. Simple, mais limite le contenu autorisé.
- **Préfixe de longueur** (paire 2). On écrit d'abord la taille du
  message (4 octets en network byte order), puis le contenu. Plus
  général, sans contrainte sur le contenu, mais ajoute du code de
  sérialisation.
- **`socket.makefile()`** (paire 3). Encapsule le flux dans un objet
  *file-like* qui gère lui-même la bufferisation et la lecture ligne
  par ligne. C'est la base sur laquelle reposent
  `socketserver.StreamRequestHandler` (dossier 03) et la plupart des
  protocoles textuels (HTTP, SMTP, IRC…).

## Limites volontaires

- **Concurrence** : un client à la fois (dossier 07).
- **Erreurs** : minimales, traitées au cas par cas.
- **TLS** : pas de chiffrement (dossier 11).

## Validation et mise en pratique

- `QUIZ.md` : 6 questions courtes d'auto-évaluation.
- `EXERCICES.md` : 8 ateliers pratiques de synthèse.
