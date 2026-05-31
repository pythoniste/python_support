# Etape 05 -- Ingestion asynchrone

## Contexte

Le pipeline lit maintenant des fichiers en parallele avec des processus. Mais la lecture I/O (disque, reseau) est mieux geree par `asyncio` : pas de processus lourds, pas de serialisation. Vous allez reecrire la couche d'ingestion en **full async** avec `asyncio` et `aiofiles`.

## Consignes

1. Creer `src/pipeline/async_reader.py` :
   - `async parse_csv_async(path: Path) -> list[SensorReading]` : lit un fichier CSV de facon asynchrone avec `aiofiles` et construit les `SensorReading`. Les lignes invalides sont loggees et ignorees.
   - `async read_all_csv_async(inbox: Path) -> list[SensorReading]` : utilise `asyncio.gather` pour lire tous les CSV en parallele. Retourne la liste aplatie.

2. Creer `src/pipeline/async_writer.py` :
   - `async write_json_async(readings: list[SensorReading], path: Path) -> None` : ecrit le JSON de facon asynchrone.

3. Adapter `src/pipeline/__main__.py` :
   - Ajouter un flag `--async` qui bascule entre le mode processus (etape 03) et le mode async.
   - Le mode async utilise `asyncio.run()` comme point d'entree.

4. Ajouter la dependance `aiofiles` dans `pyproject.toml`.

## Criteres d'acceptation

- [ ] `parse_csv_async` est une vraie coroutine (`async def`).
- [ ] `read_all_csv_async` utilise `asyncio.gather` pour la concurrence.
- [ ] Le mode `--async` fonctionne de bout en bout.
- [ ] Les tests async utilisent `pytest-asyncio`.
- [ ] `pytest tests/` est vert.

## Temps estime

1 h 30.

## Solution

Voir `solution/`.

## Pieges frequents

- **Oublier `await`** sur les appels asynchrones : la coroutine n'est pas executee, aucune erreur a la compilation.
- **Bloquer l'event loop** : ne pas appeler `open()` synchrone dans une coroutine, utiliser `aiofiles.open()`.
- **`asyncio.gather` sans gestion d'erreur** : si un fichier echoue, tout `gather` echoue. Utiliser `return_exceptions=True` ou enrober chaque appel.
- **Mixer sync et async** : ne pas appeler `asyncio.run()` dans une coroutine deja en cours.
