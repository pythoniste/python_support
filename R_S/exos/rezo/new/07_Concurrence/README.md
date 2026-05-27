# 07_Concurrence — Servir plusieurs clients en parallèle

Premier dossier qui traite la **scalabilité** : comment un serveur
peut-il gérer plusieurs clients en même temps ?

On garde le même service trivial (echo ligne par ligne) et on
compare **quatre approches** sur la même mesure de charge :

| Serveur                  | Approche                                          |
|--------------------------|---------------------------------------------------|
| `01_iteratif_srv.py`     | Itératif — un client à la fois (baseline)         |
| `02_thread_srv.py`       | Multi-thread (`ThreadingTCPServer`)               |
| `03_selectors_srv.py`    | Multiplexage I/O (module `selectors`)             |
| `04_asyncio_srv.py`      | Coroutines (`asyncio.start_server`)               |

Et un client lent (5 messages avec 0,3 s entre chacun) qu'on lance
en plusieurs exemplaires en parallèle pour mesurer la différence.

## Comment exécuter

Toutes les paires utilisent le port `8808`. Un seul serveur à la fois.

```
# Démarrer un serveur (au choix)
python3 01_iteratif_srv.py   # ou 02, 03, 04

# Dans un autre terminal — un client lent
python3 05_clt_lent.py Alice

# Pour le test de charge à 3 clients
python3 06_charge_test.py
```

## Le test de charge

Le script `06_charge_test.py` lance **3 clients en parallèle**.
Chaque client envoie 5 messages avec 0,3 s d'attente entre chacun,
soit ~1,5 s par client.

- **Serveur itératif** : les clients sont sériés → ~4,5 s.
- **Serveurs concurrents** (threads, selectors, asyncio) : en
  parallèle → ~1,5 s.

C'est le passage de l'un à l'autre qui rend la concurrence visible.

## Ce qui est démontré

- **Itératif** : limite fondamentale. Un client lent bloque tous les
  autres.
- **Multi-thread** : un thread par client. Simple, scalable jusqu'à
  quelques milliers de clients. La GIL n'est pas un problème pour
  un service I/O-bound.
- **Selectors** : un seul thread, plusieurs sockets surveillés par
  `select`/`epoll`. Économe en RAM, code moins lisible (callbacks
  ou boucle explicite).
- **Asyncio** : coroutines + boucle d'événements. Code aussi lisible
  que le synchrone (`async def`/`await`), aussi performant que
  selectors.

## Quand utiliser quoi

| Approche      | Forces                                | Faiblesses                       |
|---------------|---------------------------------------|----------------------------------|
| Itératif      | Simplicité maximale                   | Inadapté à toute charge          |
| Multi-thread  | Code synchrone facile à raisonner     | Coûteux en RAM (~1 MB / thread) |
| Selectors     | Très économe, contrôle fin            | Code en callbacks ou boucle     |
| Asyncio       | Lisible + performant, standard moderne | Tout le code doit être `async`  |

Règle de pouce 2026 :
- **moins de ~100 clients simultanés** → multi-thread suffit.
- **plus de ~1000 clients simultanés** → asyncio (ou selectors si on
  veut zéro dépendance).

## Validation et mise en pratique

- `QUIZ.md` : 6 questions sur la concurrence en Python.
- `EXERCICES.md` : 8 ateliers — pool de threads, timeout asyncio,
  test de débit comparatif, …
- `GUIDE_FORMATEUR.md` : plan détaillé pour l'intervenant.
