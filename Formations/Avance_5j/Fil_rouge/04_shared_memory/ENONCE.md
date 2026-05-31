# Etape 04 -- Shared memory

## Contexte

Avec `ProcessPoolExecutor`, chaque processus recoit une **copie** des donnees (serialisation pickle). Pour de gros volumes, cette copie coute cher en memoire et en temps. Vous allez utiliser `multiprocessing.shared_memory` pour partager un buffer de temperatures entre processus sans copie.

## Consignes

1. Creer `src/pipeline/shared.py` :
   - `create_shared_temperatures(readings: list[SensorReading]) -> tuple[SharedMemory, int]` : alloue un `SharedMemory` contenant un tableau de `float64` (les temperatures), retourne le handle et le nombre d'elements.
   - `read_shared_temperatures(shm_name: str, count: int) -> list[float]` : ouvre le `SharedMemory` existant par son nom et lit les temperatures.
   - `compute_stats_on_shared(shm_name: str, count: int) -> dict[str, float]` : calcule moyenne, ecart-type, min, max sur le buffer partage. Cette fonction est destinee a tourner dans un processus enfant.
   - `cleanup_shared(shm: SharedMemory) -> None` : ferme et detruit proprement le `SharedMemory`.

2. Adapter `src/pipeline/__main__.py` :
   - Apres la lecture parallele, stocker les temperatures en shared memory.
   - Lancer `compute_stats_on_shared` dans un processus enfant via `Process`.
   - Afficher les stats et nettoyer le shared memory.

3. Ajouter des primitives de synchronisation :
   - Utiliser un `multiprocessing.Event` pour signaler au processus parent que le calcul est termine.

## Criteres d'acceptation

- [ ] `SharedMemory` est correctement alloue et libere (pas de `ResourceWarning`).
- [ ] `compute_stats_on_shared` tourne dans un processus separe et renvoie les stats via une `Queue`.
- [ ] Le `Event` synchronise correctement parent et enfant.
- [ ] Le code gere le cas ou le shared memory n'existe plus (try/except propre).
- [ ] `pytest tests/` est vert.

## Temps estime

1 h 30.

## Solution

Voir `solution/`.

## Pieges frequents

- **Oublier `shm.close()` et `shm.unlink()`** : fuite de memoire partagee. `close()` dans chaque processus, `unlink()` une seule fois (le createur).
- **Confondre `close` et `unlink`** : `close` detache le processus, `unlink` detruit la ressource.
- **Buffer trop petit** : il faut allouer `count * 8` octets pour des `float64`.
- **Ne pas gerer `FileNotFoundError`** quand le shared memory a deja ete detruit.
