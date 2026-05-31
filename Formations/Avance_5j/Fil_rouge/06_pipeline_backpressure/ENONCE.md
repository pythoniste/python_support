# Etape 06 -- Pipeline avec backpressure

## Contexte

L'ingestion async lit tous les fichiers d'un coup et accumule les resultats en memoire. Si 10 000 fichiers arrivent, la memoire explose. Vous allez structurer le pipeline en **etages** connectes par des `asyncio.Queue` bornees, avec **backpressure** naturelle : un producteur qui va trop vite est automatiquement ralenti quand la queue est pleine.

## Consignes

1. Creer `src/pipeline/stages.py` :
   - `async ingest_stage(inbox: Path, out_queue: asyncio.Queue) -> None` : surveille le dossier `inbox/`, lit chaque nouveau CSV et pousse les `SensorReading` dans `out_queue`. S'arrete quand il recoit un signal (sentinelle `None`).
   - `async transform_stage(in_queue: asyncio.Queue, out_queue: asyncio.Queue, plugins: list[TransformPlugin]) -> None` : tire les lectures de `in_queue`, applique les plugins, pousse dans `out_queue`.
   - `async write_stage(in_queue: asyncio.Queue, outbox: Path) -> None` : tire les lectures de `in_queue` et les ecrit en JSON dans `outbox/`.

2. Creer `src/pipeline/orchestrator.py` :
   - `async run_pipeline(inbox: Path, outbox: Path, plugins: list[str], queue_size: int = 10) -> None` : cree les queues bornees, lance les trois etages dans un `TaskGroup` (Python 3.11+), gere l'arret propre.
   - Implementer un **timeout** global configurable (`--timeout` en CLI).
   - Gerer la **cancellation** : si un etage echoue, les autres sont annules proprement.

3. Adapter `__main__.py` pour utiliser `run_pipeline` quand `--async` est passe.

## Criteres d'acceptation

- [ ] Les queues sont bornees (`maxsize` > 0) pour assurer la backpressure.
- [ ] Le pipeline utilise `asyncio.TaskGroup` pour la structured concurrency.
- [ ] Un timeout global annule proprement tous les etages.
- [ ] Si un etage leve une exception, les autres sont annules (pas de hang).
- [ ] Le sentinel `None` propage l'arret de bout en bout.
- [ ] `pytest tests/` est vert.

## Temps estime

2 heures.

## Solution

Voir `solution/`.

## Pieges frequents

- **Queue non bornee** (`maxsize=0`) : aucune backpressure, la memoire explose.
- **Oublier de `await queue.put(None)`** pour propager le signal d'arret : un etage reste bloque en attente.
- **`TaskGroup` et exceptions** : si une tache leve une exception dans un `TaskGroup`, les autres sont annulees via `CancelledError`. Il faut gerer ce cas dans chaque etage.
- **Ne pas consommer la queue apres annulation** : des items restent dans la queue, le `join()` ne se termine jamais.
