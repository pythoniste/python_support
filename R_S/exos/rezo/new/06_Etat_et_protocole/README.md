# 06_Etat_et_protocole — Stateful vs stateless

Premier dossier consacré à la **conception du protocole applicatif**.
Le cas métier (calcul de mensualité d'emprunt) impose plusieurs
paramètres d'entrée (capital, taux, durée) ; on compare **deux
philosophies opposées** pour les transmettre, plus la version REST
qui tranche le débat.

## Le service

Calcul de la mensualité d'un emprunt à taux fixe :

```
M = K · t/12 / (1 - (1 + t/12)^(-n))
```

avec K = capital, t = taux annuel, n = durée en mois.

Pour `K = 200 000 €`, `t = 4,75 %`, `n = 300 mois` (25 ans), on
attend `M ≈ 1 140,23 €`.

## Plan

| Paire                                       | Style de protocole                         |
|---------------------------------------------|--------------------------------------------|
| `01_stateless_srv.py` + `02_stateless_clt.py` | **Stateless** : tous les champs en 1 requête JSON |
| `03_stateful_srv.py`  + `04_stateful_clt.py`  | **Stateful** : 3 messages successifs construisent l'état |
| `05_rest_srv.py`      + `06_rest_clt.py`      | **REST** : URL `/mensualite/<K>/<t>/<n>` |

Logique métier centralisée dans `mensualite.py` (aucun code réseau).

## Comment exécuter

Toutes les paires utilisent le port `8808`. Un seul serveur à la fois.

```
# Paire 1 — stateless JSON
python3 01_stateless_srv.py    # terminal 1
python3 02_stateless_clt.py    # terminal 2

# Paire 2 — stateful
python3 03_stateful_srv.py
python3 04_stateful_clt.py

# Paire 3 — REST
python3 05_rest_srv.py
python3 06_rest_clt.py
```

## Ce qui est démontré

- **Stateless** : le serveur n'a aucune mémoire entre messages. Chaque
  requête contient tout le nécessaire. Si le client meurt, **rien
  à nettoyer**. C'est la philosophie HTTP/REST.
- **Stateful** : le serveur accumule les paramètres au fil des
  messages. **Fragile** : un client qui meurt à mi-protocole laisse
  une connexion en attente. En contrepartie, chaque message est
  petit.
- **REST** : version stateless avec sucre syntaxique HTTP. Les
  paramètres sont dans l'URL ; le serveur ne mémorise rien.

## Pourquoi pas UDP stateful ?

Le repo original tentait un serveur UDP stateful (`mensualite_udpsrv2.py`)
en stockant l'état dans un **attribut de classe** partagé. Catastrophe :
plusieurs clients en parallèle écrivaient dans la même variable.

UDP n'a pas de session — pas de notion de « connexion » pour borner
l'état per-client. C'est l'un des arguments majeurs **pour TCP** quand
on veut un protocole conversationnel.

## Validation et mise en pratique

- `QUIZ.md` : 6 questions sur stateful vs stateless.
- `EXERCICES.md` : 8 ateliers, dont mesure des round-trips, échéancier,
  cache serveur, batch multi-emprunts.
- `GUIDE_FORMATEUR.md` : plan détaillé pour l'intervenant.
