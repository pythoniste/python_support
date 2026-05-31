"""Orchestrateur du pipeline avec TaskGroup et backpressure."""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path

from pipeline.models import SensorReading
from pipeline.stages import ingest_stage, transform_stage, write_stage

logger = logging.getLogger(__name__)


async def run_pipeline(
    inbox: Path,
    outbox: Path,
    plugins: list[str],
    queue_size: int = 10,
    timeout: float | None = None,
) -> None:
    """Lance le pipeline complet avec backpressure."""
    ingest_to_transform: asyncio.Queue[SensorReading | None] = asyncio.Queue(maxsize=queue_size)
    transform_to_write: asyncio.Queue[SensorReading | None] = asyncio.Queue(maxsize=queue_size)

    # Instancier les plugins
    plugin_instances: list[object] = []
    # Note : en production, on chargerait les plugins depuis le registre

    async def _run() -> None:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(ingest_stage(inbox, ingest_to_transform))
            tg.create_task(
                transform_stage(ingest_to_transform, transform_to_write, plugin_instances)
            )
            tg.create_task(write_stage(transform_to_write, outbox))

    if timeout is not None:
        try:
            await asyncio.wait_for(_run(), timeout=timeout)
        except asyncio.TimeoutError:
            logger.warning("Pipeline interrompu par timeout apres %.1f s", timeout)
    else:
        await _run()
