"""Lecture et parsing parallele de fichiers CSV."""

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
    readings: list[SensorReading] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
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


def read_all_csv(inbox: Path, max_workers: int = 4) -> list[SensorReading]:
    """Lit tous les CSV d'un dossier en parallele avec ProcessPoolExecutor."""
    csv_files = sorted(inbox.glob("*.csv"))
    if not csv_files:
        logger.warning("Aucun fichier CSV dans %s", inbox)
        return []

    all_readings: list[SensorReading] = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(parse_csv, p): p for p in csv_files}
        for future in futures:
            try:
                readings = future.result()
                all_readings.extend(readings)
            except Exception as exc:
                logger.error("Erreur sur %s : %s", futures[future], exc)
    return all_readings
