# 07 — Sockets bloquants et non bloquants

## 7.1 Le comportement par défaut

Par défaut, un socket Python est **bloquant**. Les appels suivants
mettent le programme en pause jusqu'à ce que l'opération aboutisse :

- `accept()` : attend qu'un client se connecte.
- `connect()` : attend la fin de la poignée de main TCP.
- `recv()` / `recvfrom()` : attend qu'au moins un octet arrive.
- `send()` / `sendto()` : attend qu'il y ait de la place dans le
  tampon d'émission.

Ce comportement est parfait pour des programmes simples, mono-utilisateur.
Il devient gênant dès qu'on veut :

- gérer **plusieurs clients en même temps** ;
- éviter de bloquer indéfiniment en cas de problème réseau ;
- intégrer du réseau dans une interface graphique.

Trois modes existent pour s'en sortir.

## 7.2 Trois modes

### Mode bloquant (défaut)

```python
s = socket.socket(...)         # bloquant par défaut
s.recv(100)                    # bloque jusqu'à au moins 1 octet
```

### Mode timeout

```python
s.settimeout(5)
try:
    s.recv(100)                # lève TimeoutError après 5 secondes
except TimeoutError:
    ...
```

Compromis simple : on accepte d'attendre, mais on garantit que
l'attente ne dépasse pas un seuil. Suffisant pour la plupart des cas.

### Mode non bloquant

```python
s.setblocking(False)
try:
    s.recv(100)                # lève BlockingIOError s'il n'y a rien
except BlockingIOError:
    ...                        # rien à lire MAINTENANT, on fera autre chose
```

Permet de scruter plusieurs sockets en parallèle. C'est la base sur
laquelle reposent :

- le module `selectors` (multiplexage à un seul thread) ;
- `asyncio` (coroutines et boucle d'événements).

Le dossier `07_Concurrence/` reviendra en détail sur ces deux outils.

## 7.3 Aperçu de la suite

Pour gérer plusieurs clients, quatre approches classiques :

1. **Itératif** : un client à la fois (`01_Sockets_bas_niveau/`).
   Simple, pas scalable.
2. **Multi-thread / multi-processus** : un thread par client
   (`socketserver.ThreadingMixIn`). Simple, coûteux en mémoire.
3. **Multiplexage avec `selectors`** : un seul thread, plusieurs
   sockets en parallèle. Économe, moins lisible.
4. **`asyncio`** : `async def` / `await`, sucre syntaxique sur le
   multiplexage. Lisible, standard moderne.

Le présent module ne fait qu'introduire le vocabulaire. Le détail
viendra plus tard.

## 7.4 À retenir

- Par défaut, un socket bloque.
- `settimeout(s)` plafonne l'attente.
- `setblocking(False)` rend l'opération immédiate (lève une exception
  si rien à faire).
- Sur cette base reposent `selectors` et `asyncio`.

## Démo

Exécuter `07_demo_bloquant.py`.
