"""Shared memory pour echange inter-processus sans copie."""

from __future__ import annotations

import math
import struct
from multiprocessing.shared_memory import SharedMemory

from pipeline.models import SensorReading

_FLOAT64_SIZE = 8  # octets


def create_shared_temperatures(readings: list[SensorReading]) -> tuple[SharedMemory, int]:
    """Alloue un SharedMemory contenant les temperatures en float64."""
    count = len(readings)
    shm = SharedMemory(create=True, size=count * _FLOAT64_SIZE)
    fmt = f"{count}d"
    temps = [r.temperature for r in readings]
    struct.pack_into(fmt, shm.buf, 0, *temps)
    return shm, count


def read_shared_temperatures(shm_name: str, count: int) -> list[float]:
    """Ouvre un SharedMemory existant et lit les temperatures."""
    shm = SharedMemory(name=shm_name, create=False)
    try:
        fmt = f"{count}d"
        temps = list(struct.unpack_from(fmt, shm.buf, 0))
        return temps
    finally:
        shm.close()


def compute_stats_on_shared(shm_name: str, count: int) -> dict[str, float]:
    """Calcule moyenne, ecart-type, min, max sur le buffer partage."""
    temps = read_shared_temperatures(shm_name, count)
    mean = sum(temps) / count
    variance = sum((t - mean) ** 2 for t in temps) / count
    return {
        "mean": mean,
        "std": math.sqrt(variance),
        "min": min(temps),
        "max": max(temps),
    }


def cleanup_shared(shm: SharedMemory) -> None:
    """Ferme et detruit proprement le SharedMemory."""
    shm.close()
    shm.unlink()
