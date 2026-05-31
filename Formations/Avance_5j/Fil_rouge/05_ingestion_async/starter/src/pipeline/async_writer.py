"""Ecriture asynchrone au format JSON.

A completer : implementer write_json_async.
"""

from __future__ import annotations

import json
from pathlib import Path

import aiofiles

from pipeline.models import SensorReading


async def write_json_async(readings: list[SensorReading], path: Path) -> None:
    """Ecrit les lectures en JSON de facon asynchrone."""
    # TODO : serialiser puis ecrire avec aiofiles
    ...
