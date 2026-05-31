"""Etages du pipeline connectes par des queues bornees.

A completer : implementer ingest_stage, transform_stage, write_stage.
"""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path

from pipeline.models import SensorReading

logger = logging.getLogger(__name__)


async def ingest_stage(inbox: Path, out_queue: asyncio.Queue[SensorReading | None]) -> None:
    """Lit les CSV et pousse les SensorReading dans out_queue.

    Pousse None (sentinelle) quand tous les fichiers sont traites.
    """
    # TODO : lire chaque CSV, pousser les lectures, puis pousser None
    ...


async def transform_stage(
    in_queue: asyncio.Queue[SensorReading | None],
    out_queue: asyncio.Queue[SensorReading | None],
    plugins: list[object],
) -> None:
    """Tire les lectures de in_queue, applique les plugins, pousse dans out_queue."""
    # TODO : consommer in_queue, appliquer les plugins, propager None
    ...


async def write_stage(
    in_queue: asyncio.Queue[SensorReading | None],
    outbox: Path,
) -> None:
    """Tire les lectures de in_queue et les ecrit en JSON."""
    # TODO : consommer in_queue, ecrire par lots ou individuellement
    ...
