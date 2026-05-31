# Avancé Python — 5 jours

**Cible :** développeur Python confirmé.
**Objectif :** métaprogrammation, concurrence et asyncio, performance et profiling, sécurité de base, packaging avancé, nouveautés Python 3.14.
**Fil rouge :** 🚀 Pipeline de données asynchrone (voir `Fil_rouge/README.md`).

## Programme jour par jour

### J1 — Métaprogrammation & internals
- **Matin :** Descripteurs (`__get__`, `__set__`, `__set_name__`) · `__init_subclass__`, class decorators · Métaclasses (`type`, cas ORM)
- **Après-midi :** ABC vs `Protocol` (choix architectural) · `__slots__`, `weakref`, `gc` · Bytecode et `dis` (teaser) · `inspect`
- **Étapes fil rouge :** 01 (matin), 02 (après-midi)

### J2 — Concurrence
- **Matin :** `threading`, GIL expliqué · `multiprocessing`, `Pool`, shared memory · `concurrent.futures`
- **Après-midi :** Primitives de synchro (`Lock`, `Semaphore`, `Event`, `Queue`) · PEP 703 free-threaded Python 3.14 · Patterns producer/consumer, fan-out
- **Étapes fil rouge :** 03 (matin), 04 (après-midi)

### J3 — Asyncio complet
- **Matin :** Event loop, coroutines, tasks · `async`/`await`, `gather`, `as_completed` · `asyncio.Queue`, `Lock`, `Semaphore`
- **Après-midi :** `httpx` async, `aiohttp` · Structured concurrency (`TaskGroup`, `anyio`) · Backpressure, timeouts, cancellation
- **Étapes fil rouge :** 05 (matin), 06 (après-midi)

### J4 — Performance & profiling
- **Matin :** Profiling CPU : `cProfile`, `line_profiler`, `py-spy` · Profiling mémoire : `tracemalloc`, `memray`
- **Après-midi :** Benchmarking rigoureux (`pyperf`) · Optimisation algorithmique et structures · Cython / Numba / `mypyc` (teasers)
- **Étapes fil rouge :** 07 (matin), 08 (après-midi)

### J5 — Sécurité, packaging, nouveautés
- **Matin :** Crypto basiques : `hashlib`, `hmac` · Hachage mots de passe (`argon2-cffi`) · Module `secrets` · Chiffrement symétrique (`cryptography.fernet`)
- **Après-midi :** Logs structurés (`structlog`) · Packaging avancé (wheels, publication PyPI/TestPyPI) · **Nouveautés Python 3.11 → 3.14** · Finalisation fil rouge
- **Étapes fil rouge :** 09 (matin), 10 (après-midi)

## Fil rouge

Le dossier `Fil_rouge/` contient le projet classique (10 étapes).
