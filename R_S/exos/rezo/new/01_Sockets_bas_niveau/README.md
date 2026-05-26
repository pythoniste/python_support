# 01_Sockets_bas_niveau — Premiers clients/serveurs réels

Premier dossier de code exécutable. On met en œuvre l'API socket
exactement telle qu'introduite au dossier 00 : `socket()`, `bind()`,
`listen()`, `accept()`, `connect()`, `recv()`, `send()`.

## Plan

Quatre fichiers, deux paires client / serveur :

| Fichier         | Rôle                |
|-----------------|---------------------|
| `01_tcpsrv.py`  | Serveur TCP         |
| `02_tcpclt.py`  | Client TCP          |
| `03_udpsrv.py`  | Serveur UDP         |
| `04_udpclt.py`  | Client UDP          |

## Comment exécuter

Ouvrir deux terminaux. Démarrer d'abord le serveur, puis le client.

```
# Terminal 1
python3 01_tcpsrv.py

# Terminal 2
python3 02_tcpclt.py
```

Idem pour UDP avec `03_udpsrv.py` et `04_udpclt.py`.

Le port utilisé est `8808` pour les deux paires (les deux serveurs ne
peuvent donc pas tourner *simultanément*, mais l'un après l'autre).

## Ce qui est démontré

- Le cycle de vie complet `socket → bind → listen → accept` côté
  serveur TCP.
- Le cycle court `socket → connect` côté client TCP.
- L'absence de `listen` / `accept` côté UDP.
- L'usage systématique du `with` pour libérer les descripteurs.
- L'usage de `socket.getaddrinfo` pour résoudre l'adresse (introduit
  au module 00/01).

## Ce qui est volontairement reporté

- **Framing** (dossier 02) : ici, chaque `recv()` est supposé
  retourner un message complet. C'est vrai en local sur messages
  courts ; sur un vrai réseau, il faut un mécanisme explicite — voir
  module 00/05.
- **Concurrence** (dossier 07) : le serveur TCP ne traite qu'un seul
  client à la fois.
- **Gestion d'erreur** : minimale ici, traitée au cas par cas dans
  les dossiers suivants.

## Validation et mise en pratique

Deux fichiers complètent le code :

- **`QUIZ.md`** : six questions courtes d'auto-évaluation.
- **`EXERCICES.md`** : ateliers pratiques de synthèse.

Un guide formateur est fourni dans `GUIDE_FORMATEUR.md`.
