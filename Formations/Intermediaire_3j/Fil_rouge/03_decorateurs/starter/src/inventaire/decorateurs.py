"""Décorateurs — étape 03 (starter).

TODO : implémenter @log_action, @timer.
"""

from __future__ import annotations

import functools
import logging
import time
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__name__)


def log_action(func: Callable[..., Any]) -> Callable[..., Any]:
    raise NotImplementedError


def timer(func: Callable[..., Any]) -> Callable[..., Any]:
    raise NotImplementedError
