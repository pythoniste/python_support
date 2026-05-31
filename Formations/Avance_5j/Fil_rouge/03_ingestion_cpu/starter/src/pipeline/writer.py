"""Ecriture des resultats au format JSON.

A completer : implementer write_json.
"""

from __future__ import annotations

import json
from pathlib import Path

from pipeline.models import SensorReading


def write_json(readings: list[SensorReading], path: Path) -> None:
    """Ecrit les lectures au format JSON (liste de dicts)."""
    # TODO : serialiser les SensorReading en JSON
    ...
