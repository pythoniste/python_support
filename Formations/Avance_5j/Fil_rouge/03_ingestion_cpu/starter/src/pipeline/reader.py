"""Lecture et parsing parallele de fichiers CSV.

A completer : implementer parse_csv et read_all_csv.
"""

from __future__ import annotations

import csv
import logging
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from pipeline.models import SensorReading

logger = logging.getLogger(__name__)


def parse_csv(path: Path) -> list[SensorReading]:
    """Lit un CSV et retourne une liste de SensorReading.

    Colonnes attendues : sensor_id,temperature,humidity,pressure.
    Les lignes invalides sont ignorees avec un log warning.
    """
    # TODO : implementer la lecture CSV avec gestion des lignes invalides
    ...


def read_all_csv(inbox: Path, max_workers: int = 4) -> list[SensorReading]:
    """Lit tous les CSV d'un dossier en parallele avec ProcessPoolExecutor.

    Retourne la liste aplatie de toutes les lectures.
    """
    # TODO : utiliser ProcessPoolExecutor pour paralleliser parse_csv
    ...
