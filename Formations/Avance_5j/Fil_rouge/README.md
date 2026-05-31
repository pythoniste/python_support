# Fil rouge — Pipeline de donnees asynchrone

## Contexte metier

Votre entreprise recoit un flux continu de fichiers CSV de capteurs IoT (temperature, humidite, pression). Les fichiers arrivent dans un repertoire `inbox/`, doivent etre valides, transformes (moyenne glissante, detection d'anomalies), puis ecrits dans un repertoire `outbox/` au format JSON. Le volume augmente : il faut traiter **des centaines de fichiers par minute** sans exploser la memoire.

Vous allez construire un **pipeline de donnees** qui :

- lit et valide les CSV entrants ;
- applique des transformations configurables via un systeme de plugins ;
- exploite le parallelisme CPU et l'asynchrone I/O ;
- gere la backpressure (ne pas saturer la memoire si les fichiers arrivent plus vite qu'on ne les traite) ;
- est profile, securise (hachage d'integrite), et distribue sous forme de package observable.

Ce projet vous accompagne sur les 5 jours de la formation Avance. A chaque demi-journee, vous enrichissez le pipeline d'une nouvelle capacite. A la fin du J5, vous disposez d'un **package Python distributable** avec plugins, concurrence, observabilite et securite.

## Structure des etapes

Chaque dossier `NN_titre/` contient :

- **`ENONCE.md`** : les consignes, attendus et criteres d'acceptation de l'etape.
- **`starter/`** : un projet de depart avec `pyproject.toml`, un squelette de `src/pipeline/`, et des tests pytest deja ecrits. Vous implementez le code manquant jusqu'a ce que les tests passent.
- **`solution/`** : une proposition de solution **complete et cumulative**. Elle contient le projet entier a ce stade, pas seulement un diff. A consulter **apres** tentative personnelle.

## Progression

| # | Moment | Etape | Livrable de l'etape |
|---|---|---|---|
| 01 | J1 matin | Descripteurs | Champs valides via descripteurs (`__set_name__`, `__get__`, `__set__`) |
| 02 | J1 apres-midi | Plugins | Systeme de plugins par `__init_subclass__` et entry points |
| 03 | J2 matin | Ingestion CPU | Lecture parallele des CSV avec `ProcessPoolExecutor` |
| 04 | J2 apres-midi | Shared memory | Echange de donnees entre processus via `shared_memory` |
| 05 | J3 matin | Ingestion async | Lecture async des fichiers avec `asyncio` + `aiofiles` |
| 06 | J3 apres-midi | Pipeline backpressure | `asyncio.Queue` bornee, `TaskGroup`, timeouts, cancellation |
| 07 | J4 matin | Profiling CPU | `cProfile`, `line_profiler`, `py-spy` sur le pipeline |
| 08 | J4 apres-midi | Profiling memoire | `tracemalloc`, `memray`, optimisation des allocations |
| 09 | J5 matin | Securisation | Hachage d'integrite, `hmac`, chiffrement Fernet des sorties |
| 10 | J5 apres-midi | Packaging et observabilite | `structlog`, metrics, wheel distribuable, finalisation |

## Livrable final (fin J5)

A la fin de l'etape 10, vous devez pouvoir executer :

```bash
cd 10_packaging_observabilite/solution
uv build
uv pip install dist/pipeline-*.whl
pipeline --inbox data/inbox --outbox data/outbox   # lance le pipeline
pytest                                              # tous les tests passent
ruff check .                                        # aucune erreur de lint
```

## Comment utiliser ce fil rouge ?

1. **Lire l'`ENONCE.md`** de l'etape en cours.
2. **Copier le `starter/`** ailleurs (par exemple dans un dossier `mon_travail/` a cote). C'est votre espace de travail.
3. **Implementer** le code manquant. Lancer `pytest` regulierement pour verifier votre progression.
4. **Comparer avec `solution/`** une fois termine (ou apres 45 minutes de recherche infructueuse -- pas avant !).
5. **Passer a l'etape suivante** en repartant de votre code si tout est vert, ou de la `solution/` precedente si vous avez pris du retard.

Bon courage !
