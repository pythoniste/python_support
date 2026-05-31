"""Utilitaires de profiling CPU."""

from __future__ import annotations

import cProfile
import io
import pstats
from typing import Any, Callable


def profile_with_cprofile(func: Callable[..., Any], *args: Any, **kwargs: Any) -> pstats.Stats:
    """Execute une fonction sous cProfile et retourne les stats."""
    profiler = cProfile.Profile()
    profiler.enable()
    func(*args, **kwargs)
    profiler.disable()
    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    return stats


def print_top_functions(stats: pstats.Stats, n: int = 20) -> None:
    """Affiche les N fonctions les plus couteuses."""
    stats.sort_stats("cumulative")
    stats.print_stats(n)
