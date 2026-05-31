"""Orchestrateur du pipeline avec TaskGroup et backpressure.

A completer : implementer run_pipeline.
"""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


async def run_pipeline(
    inbox: Path,
    outbox: Path,
    plugins: list[str],
    queue_size: int = 10,
    timeout: float | None = None,
) -> None:
    """Lance le pipeline complet avec backpressure.

    Cree les queues bornees, lance les trois etages dans un TaskGroup,
    gere le timeout et la cancellation.
    """
    # TODO : creer les queues, lancer les stages dans un TaskGroup
    # TODO : gerer le timeout global
    ...
