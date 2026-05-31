"""Etages du pipeline connectes par des queues bornees."""

from __future__ import annotations

import asyncio
import json
import logging
from pathlib import Path

import aiofiles

from pipeline.async_reader import parse_csv_async
from pipeline.models import SensorReading

logger = logging.getLogger(__name__)


async def ingest_stage(inbox: Path, out_queue: asyncio.Queue[SensorReading | None]) -> None:
    """Lit les CSV et pousse les SensorReading dans out_queue."""
    csv_files = sorted(inbox.glob("*.csv"))
    for csv_path in csv_files:
        try:
            readings = await parse_csv_async(csv_path)
            for reading in readings:
                await out_queue.put(reading)
            logger.info("Ingere %d lectures de %s", len(readings), csv_path.name)
        except Exception as exc:
            logger.error("Erreur sur %s : %s", csv_path, exc)
    await out_queue.put(None)  # sentinelle


async def transform_stage(
    in_queue: asyncio.Queue[SensorReading | None],
    out_queue: asyncio.Queue[SensorReading | None],
    plugins: list[object],
) -> None:
    """Tire les lectures de in_queue, applique les plugins, pousse dans out_queue."""
    batch: list[SensorReading] = []
    while True:
        item = await in_queue.get()
        if item is None:
            # Traiter le dernier lot
            if batch:
                transformed = batch
                for plugin in plugins:
                    transformed = plugin.transform(transformed)  # type: ignore[attr-defined]
                for reading in transformed:
                    await out_queue.put(reading)
            await out_queue.put(None)  # propager sentinelle
            break
        batch.append(item)
        if len(batch) >= 100:
            transformed = batch
            for plugin in plugins:
                transformed = plugin.transform(transformed)  # type: ignore[attr-defined]
            for reading in transformed:
                await out_queue.put(reading)
            batch = []


async def write_stage(
    in_queue: asyncio.Queue[SensorReading | None],
    outbox: Path,
) -> None:
    """Tire les lectures de in_queue et les ecrit en JSON."""
    outbox.mkdir(parents=True, exist_ok=True)
    all_readings: list[dict[str, object]] = []
    while True:
        item = await in_queue.get()
        if item is None:
            break
        all_readings.append({
            "sensor_id": item.sensor_id,
            "temperature": item.temperature,
            "humidity": item.humidity,
            "pressure": item.pressure,
        })
    if all_readings:
        output_path = outbox / "output.json"
        content = json.dumps(all_readings, indent=2, ensure_ascii=False)
        async with aiofiles.open(output_path, mode="w", encoding="utf-8") as f:
            await f.write(content)
        logger.info("Ecrit %d lectures dans %s", len(all_readings), output_path)
