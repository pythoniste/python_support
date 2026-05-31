# Etape 07 -- Profiling CPU

## Contexte

Le pipeline fonctionne, mais est-il rapide ? Ou passe-t-il son temps ? Avant d'optimiser, il faut **mesurer**. Vous allez profiler le pipeline avec `cProfile`, `line_profiler` et `py-spy` pour identifier les goulots d'etranglement CPU.

## Consignes

1. Creer `src/pipeline/profiling.py` :
   - `profile_with_cprofile(func: Callable, *args, **kwargs) -> pstats.Stats` : execute une fonction sous `cProfile` et retourne les stats.
   - `print_top_functions(stats: pstats.Stats, n: int = 20) -> None` : affiche les N fonctions les plus couteuses, triees par temps cumule.

2. Creer `scripts/profile_pipeline.py` :
   - Script autonome qui genere 100 fichiers CSV de test (1000 lignes chacun).
   - Profile le pipeline complet (lecture -> transformation -> ecriture) avec `cProfile`.
   - Sauvegarde le profil dans `profiling_results/pipeline.prof`.
   - Affiche les 20 fonctions les plus couteuses.

3. Creer `scripts/profile_line.py` :
   - Profile la fonction `parse_csv` avec `line_profiler` (decorateur `@profile` ou API programmatique).
   - Affiche le temps ligne par ligne.

4. Documenter dans un fichier `PROFILING_NOTES.md` (a la racine de l'etape) :
   - Les commandes pour lancer `py-spy` sur le pipeline.
   - Comment generer un flamegraph SVG.
   - Les 3 goulots identifies et les pistes d'optimisation.

## Criteres d'acceptation

- [ ] `profile_with_cprofile` retourne des `pstats.Stats` exploitables.
- [ ] Le script genere les fichiers de test et profile le pipeline.
- [ ] Le fichier `.prof` est lisible avec `snakeviz` ou `pstats`.
- [ ] `PROFILING_NOTES.md` contient les commandes `py-spy` et les goulots identifies.
- [ ] `pytest tests/` est vert (les tests ne profilent pas, mais verifient que les fonctions de profiling marchent).

## Temps estime

1 h 30.

## Solution

Voir `solution/`.

## Pieges frequents

- **Profiler en mode debug** : le profiling ralentit l'execution. Ne pas comparer des temps profiles avec des temps non-profiles.
- **`cProfile` et async** : `cProfile` ne suit pas bien les coroutines. Pour profiler du code async, utiliser `py-spy` en mode sampling.
- **`line_profiler` et decorateur** : le decorateur `@profile` n'existe que si le script est lance via `kernprof`. En import normal, ca plante.
- **Oublier de trier les stats** : `print_stats()` sans `sort_stats()` affiche dans un ordre inutile.
