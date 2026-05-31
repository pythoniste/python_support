"""Lecture asynchrone de fichiers CSV.

A completer : implementer parse_csv_async et read_all_csv_async.
"""

from __future__ import annotations

import csv
import io
import logging
from pathlib import Path

import aiofiles

from pipeline.models import SensorReading

logger = logging.getLogger(__name__)


async def parse_csv_async(path: Path) -> list[SensorReading]:
    """Lit un CSV de facon asynchrone et construit les SensorReading."""
    # TODO : utiliser aiofiles.open pour lire, puis csv.DictReader sur le contenu
    ...


async def read_all_csv_async(inbox: Path) -> list[SensorReading]:
    """Lit tous les CSV en parallele avec asyncio.gather."""
    # TODO : utiliser asyncio.gather sur parse_csv_async
    ...
