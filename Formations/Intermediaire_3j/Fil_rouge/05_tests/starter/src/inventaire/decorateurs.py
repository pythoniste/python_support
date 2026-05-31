"""Décorateurs métier de l'inventaire IT."""

from __future__ import annotations

import functools
import logging
import time
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__name__)


def log_action(func: Callable[..., Any]) -> Callable[..., Any]:
    """Logge chaque appel."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.debug("Appel %s(args=%s, kwargs=%s)", func.__name__, args, kwargs)
        result = func(*args, **kwargs)
        logger.debug("Retour %s -> %s", func.__name__, result)
        return result
    return wrapper


def timer(func: Callable[..., Any]) -> Callable[..., Any]:
    """Mesure et logge le temps d'exécution."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.debug("%s a pris %.4f s", func.__name__, elapsed)
        return result
    return wrapper
