# Etape 08 -- Profiling memoire

## Contexte

Le pipeline traite des volumes croissants. Vous avez identifie les goulots CPU a l'etape precedente. Maintenant, il faut verifier que la **memoire** n'explose pas. Vous allez utiliser `tracemalloc` et `memray` pour traquer les allocations et optimiser.

## Consignes

1. Creer `src/pipeline/mem_profiling.py` :
   - `trace_memory(func: Callable, *args, **kwargs) -> tuple[Any, list[tracemalloc.Statistic]]` : execute une fonction avec `tracemalloc` actif et retourne le resultat + les top 10 allocations.
   - `print_memory_stats(stats: list[tracemalloc.Statistic], n: int = 10) -> None` : affiche les N plus grosses allocations avec fichier et ligne.

2. Creer `scripts/profile_memory.py` :
   - Genere 50 fichiers CSV de test (10 000 lignes chacun).
   - Mesure la memoire du pipeline avec `tracemalloc`.
   - Affiche les allocations les plus couteuses.
   - Compare avant/apres optimisation.

3. Optimiser `SensorReading` avec `__slots__` :
   - Ajouter `__slots__` a `SensorReading` pour reduire l'empreinte memoire.
   - **Attention** : les descripteurs doivent continuer a fonctionner avec `__slots__`. Il faudra adapter le stockage (utiliser un slot dedie ou un `WeakKeyDictionary`).

4. Documenter dans `MEMORY_NOTES.md` :
   - Commandes pour lancer `memray` et generer le flamegraph memoire.
   - Comparaison avant/apres `__slots__` (nombre d'octets par instance).
   - Autres pistes d'optimisation (generateurs au lieu de listes, etc.).

## Criteres d'acceptation

- [ ] `tracemalloc` capture les allocations du pipeline.
- [ ] `SensorReading` avec `__slots__` utilise moins de memoire (verifiable par `sys.getsizeof`).
- [ ] Les descripteurs fonctionnent toujours apres l'ajout de `__slots__`.
- [ ] `MEMORY_NOTES.md` contient les resultats compares.
- [ ] `pytest tests/` est vert.

## Temps estime

1 h 30.

## Solution

Voir `solution/`.

## Pieges frequents

- **`__slots__` et descripteurs** : avec `__slots__`, `instance.__dict__` n'existe plus. Le descripteur doit stocker la valeur ailleurs (dans un slot dedie ou via un mapping externe).
- **`tracemalloc` et multiprocessing** : `tracemalloc` ne suit que le processus courant. Pour les sous-processus, il faut l'activer dans chaque processus enfant.
- **Mesurer `sys.getsizeof` sur des conteneurs** : ca ne mesure que l'objet lui-meme, pas les objets references. Utiliser `pympler.asizeof` pour la taille profonde.
- **Generateurs et memoire** : un generateur ne stocke qu'un element a la fois, mais si vous faites `list(generateur)`, vous rematerialisez tout en memoire.
