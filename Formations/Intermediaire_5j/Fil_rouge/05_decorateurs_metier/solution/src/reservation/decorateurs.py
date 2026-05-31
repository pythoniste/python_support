"""Décorateurs métier du système de réservation."""

from __future__ import annotations

import functools
import logging
import time
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__name__)


def log_appel(func: Callable[..., Any]) -> Callable[..., Any]:
    """Logge chaque appel : nom, arguments, résultat."""

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


def autoriser(roles: list[str]) -> Callable[..., Any]:
    """Décorateur paramétré : vérifie le rôle de l'utilisateur (1er arg)."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not args:
                raise TypeError(f"{func.__name__} attend un utilisateur en premier argument.")
            utilisateur = args[0]
            role = getattr(utilisateur, "role", "user")
            if role not in roles:
                raise PermissionError(
                    f"{utilisateur.nom} (rôle={role!r}) n'a pas la permission "
                    f"d'appeler {func.__name__}. Rôles requis : {roles}"
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator
