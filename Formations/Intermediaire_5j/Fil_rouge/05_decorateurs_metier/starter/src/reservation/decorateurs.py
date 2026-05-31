"""Décorateurs métier — étape 05 (starter).

TODO : implémenter @log_appel, @timer, @autoriser(roles).
"""

from __future__ import annotations

import functools
import logging
import time
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__name__)


def log_appel(func: Callable[..., Any]) -> Callable[..., Any]:
    """Logge chaque appel : nom, arguments, résultat."""
    raise NotImplementedError


def timer(func: Callable[..., Any]) -> Callable[..., Any]:
    """Mesure et logge le temps d'exécution."""
    raise NotImplementedError


def autoriser(roles: list[str]) -> Callable[..., Any]:
    """Décorateur paramétré : vérifie le rôle de l'utilisateur (1er arg)."""
    raise NotImplementedError
