"""Ecriture des resultats au format JSON."""

from __future__ import annotations

import json
from pathlib import Path

from pipeline.models import SensorReading


def write_json(readings: list[SensorReading], path: Path) -> None:
    """Ecrit les lectures au format JSON (liste de dicts)."""
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
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
