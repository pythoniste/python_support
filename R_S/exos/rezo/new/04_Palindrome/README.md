# 04_Palindrome — Cinq façons d'exposer la même logique métier

Premier dossier centré sur un **cas d'usage métier** : détecter qu'une
chaîne est un palindrome (« Karine alla en Irak », « Esope reste ici
et se repose », etc.). On utilise cet exercice pour comparer
**côte à côte** les cinq mécanismes vus jusqu'à présent :

| Paire                                       | Couche                                     |
|---------------------------------------------|--------------------------------------------|
| `01_raw_tcp_srv.py` + `02_raw_tcp_clt.py`   | TCP raw + framing par délimiteur (dossier 02) |
| `03_raw_udp_srv.py` + `04_raw_udp_clt.py`   | UDP raw                                    |
| `05_ss_tcp_srv.py`  + `06_ss_tcp_clt.py`    | socketserver TCP                           |
| `07_ss_udp_srv.py`  + `08_ss_udp_clt.py`    | socketserver UDP                           |
| `09_bottle_palindrome.py` + `10_bottle_clt.py` | HTTP/REST via Bottle + `requests`      |

La **logique métier** est centralisée dans `palindrome.py`, importée
par les cinq variantes — l'exercice porte sur la *transport layer*,
pas sur l'algorithme.

## Comment exécuter

Toutes les paires utilisent le port `8808`. Un seul serveur à la fois.

```
# Paire 1 — TCP raw
python3 01_raw_tcp_srv.py    # terminal 1
python3 02_raw_tcp_clt.py    # terminal 2

# Paire 5 — Bottle REST
python3 09_bottle_palindrome.py    # terminal 1
python3 10_bottle_clt.py           # terminal 2  (ou curl en ligne de commande)
```

## Protocole applicatif

Côté TCP/UDP : le client envoie un mot (terminé par `\n` en TCP),
le serveur répond par l'un des trois codes textuels :

- `PALINDROME`     : le mot est un palindrome
- `PAS_PALINDROME` : non
- `ARRET`          : le mot-clé spécial `stop` a été reçu, le serveur s'arrête

Côté Bottle : `GET /palindrome/<mot>` renvoie un JSON
`{"mot": "...", "est_palindrome": true|false}`.

## Pourquoi cinq variantes du même service ?

L'intérêt pédagogique est précisément la **comparaison** :

- même logique métier (`palindrome.py`) ;
- cinq lignes de transport différentes ;
- complexité du code utile très contrastée ;
- comportement face à la charge, aux erreurs, et à la latence différent.

À la fin du dossier, on saura **choisir** entre ces transports en
fonction du contexte. C'est l'objectif du quiz.

## Limites volontaires

- **Concurrence** : un client à la fois sur les serveurs raw et
  socketserver standard (dossier 07).
- **Encodage** : on reste sur UTF-8 implicite (dossier 11/TLS et
  dossier i18n plus tard).
- **Sécurité** : pas d'authentification, le service est public sur
  127.0.0.1.

## Validation et mise en pratique

- `QUIZ.md` : 6 questions sur les choix de transport.
- `EXERCICES.md` : 8 ateliers de consolidation et d'extension.
- `GUIDE_FORMATEUR.md` : plan détaillé pour l'intervenant.
