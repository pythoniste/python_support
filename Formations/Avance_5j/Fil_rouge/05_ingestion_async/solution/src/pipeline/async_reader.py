"""Lecture asynchrone de fichiers CSV."""

from __future__ import annotations

import asyncio
import csv
import io
import logging
from pathlib import Path

import aiofiles

from pipeline.models import SensorReading

logger = logging.getLogger(__name__)


async def parse_csv_async(path: Path) -> list[SensorReading]:
    """Lit un CSV de facon asynchrone et construit les SensorReading."""
    readings: list[SensorReading] = []
    async with aiofiles.open(path, mode="r", encoding="utf-8") as f:
        content = await f.read()
    reader = csv.DictReader(io.StringIO(content))
    for line_no, row in enumerate(reader, start=2):
        try:
            reading = SensorReading(
                sensor_id=row["sensor_id"],
                temperature=float(row["temperature"]),
                humidity=float(row["humidity"]),
                pressure=float(row["pressure"]),
            )
            readings.append(reading)
        except (ValueError, KeyError) as exc:
            logger.warning("Ligne %d de %s ignoree : %s", line_no, path.name, exc)
    return readings


async def read_all_csv_async(inbox: Path) -> list[SensorReading]:
    """Lit tous les CSV en parallele avec asyncio.gather."""
    csv_files = sorted(inbox.glob("*.csv"))
    if not csv_files:
        logger.warning("Aucun fichier CSV dans %s", inbox)
        return []
    results = await asyncio.gather(
        *(parse_csv_async(p) for p in csv_files),
        return_exceptions=True,
    )
    all_readings: list[SensorReading] = []
    for result, path in zip(results, csv_files):
        if isinstance(result, Exception):
            logger.error("Erreur sur %s : %s", path, result)
        else:
            all_readings.extend(result)
    return all_readings
