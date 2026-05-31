"""Ecriture asynchrone au format JSON."""

from __future__ import annotations

import json
from pathlib import Path

import aiofiles

from pipeline.models import SensorReading


async def write_json_async(readings: list[SensorReading], path: Path) -> None:
    """Ecrit les lectures en JSON de facon asynchrone."""
    data = [
        {
            "sensor_id": r.sensor_id,
            "temperature": r.temperature,
            "humidity": r.humidity,
            "pressure": r.pressure,
        }
        for r in readings
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(data, indent=2, ensure_ascii=False)
    async with aiofiles.open(path, mode="w", encoding="utf-8") as f:
        await f.write(content)
