"""Utilitaires de profiling memoire.

A completer : implementer trace_memory et print_memory_stats.
"""

from __future__ import annotations

import tracemalloc
from typing import Any, Callable


def trace_memory(
    func: Callable[..., Any], *args: Any, **kwargs: Any
) -> tuple[Any, list[tracemalloc.Statistic]]:
    """Execute une fonction avec tracemalloc actif.

    Retourne (resultat, top_10_allocations).
    """
    # TODO : tracemalloc.start(), executer, take_snapshot, compare
    ...


def print_memory_stats(stats: list[tracemalloc.Statistic], n: int = 10) -> None:
    """Affiche les N plus grosses allocations."""
    # TODO : iterer et afficher
    ...
