"""Shared memory pour echange inter-processus sans copie.

A completer : implementer create_shared_temperatures, read_shared_temperatures,
compute_stats_on_shared, cleanup_shared.
"""

from __future__ import annotations

import struct
from multiprocessing.shared_memory import SharedMemory
from pathlib import Path

from pipeline.models import SensorReading


def create_shared_temperatures(readings: list[SensorReading]) -> tuple[SharedMemory, int]:
    """Alloue un SharedMemory contenant les temperatures en float64.

    Retourne (shm, count).
    """
    # TODO : allouer count * 8 octets, ecrire les temperatures avec struct.pack
    ...


def read_shared_temperatures(shm_name: str, count: int) -> list[float]:
    """Ouvre un SharedMemory existant et lit les temperatures."""
    # TODO : ouvrir le shm par nom, lire avec struct.unpack
    ...


def compute_stats_on_shared(shm_name: str, count: int) -> dict[str, float]:
    """Calcule moyenne, ecart-type, min, max sur le buffer partage.

    Destinee a tourner dans un processus enfant.
    """
    # TODO : lire les temperatures et calculer les stats
    ...


def cleanup_shared(shm: SharedMemory) -> None:
    """Ferme et detruit proprement le SharedMemory."""
    # TODO : close + unlink
    ...
