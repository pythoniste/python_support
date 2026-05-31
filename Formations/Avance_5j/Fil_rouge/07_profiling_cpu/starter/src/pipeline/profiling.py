"""Utilitaires de profiling CPU.

A completer : implementer profile_with_cprofile et print_top_functions.
"""

from __future__ import annotations

import cProfile
import pstats
from typing import Any, Callable


def profile_with_cprofile(func: Callable[..., Any], *args: Any, **kwargs: Any) -> pstats.Stats:
    """Execute une fonction sous cProfile et retourne les stats."""
    # TODO : utiliser cProfile.Profile, run la fonction, retourner pstats.Stats
    ...


def print_top_functions(stats: pstats.Stats, n: int = 20) -> None:
    """Affiche les N fonctions les plus couteuses."""
    # TODO : sort_stats('cumulative') et print_stats(n)
    ...
