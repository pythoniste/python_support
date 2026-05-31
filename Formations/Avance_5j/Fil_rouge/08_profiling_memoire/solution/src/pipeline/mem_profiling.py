"""Utilitaires de profiling memoire."""

from __future__ import annotations

import tracemalloc
from typing import Any, Callable


def trace_memory(
    func: Callable[..., Any], *args: Any, **kwargs: Any
) -> tuple[Any, list[tracemalloc.Statistic]]:
    """Execute une fonction avec tracemalloc actif."""
    tracemalloc.start()
    snapshot_before = tracemalloc.take_snapshot()
    result = func(*args, **kwargs)
    snapshot_after = tracemalloc.take_snapshot()
    tracemalloc.stop()
    stats = snapshot_after.compare_to(snapshot_before, "lineno")
    return result, stats[:10]


def print_memory_stats(stats: list[tracemalloc.Statistic], n: int = 10) -> None:
    """Affiche les N plus grosses allocations."""
    for i, stat in enumerate(stats[:n], start=1):
        print(f"#{i}: {stat}")
