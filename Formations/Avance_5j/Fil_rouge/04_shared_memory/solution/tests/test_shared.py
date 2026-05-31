"""Tests pour le shared memory."""

import pytest

from pipeline.models import SensorReading
from pipeline.shared import (
    cleanup_shared,
    compute_stats_on_shared,
    create_shared_temperatures,
    read_shared_temperatures,
)


@pytest.fixture()
def readings() -> list[SensorReading]:
    return [
        SensorReading("AB-1234", 20.0 + i, 50.0, 1013.0)
        for i in range(10)
    ]


class TestSharedMemory:
    def test_create_and_read(self, readings: list[SensorReading]) -> None:
        shm, count = create_shared_temperatures(readings)
        try:
            assert count == 10
            temps = read_shared_temperatures(shm.name, count)
            assert len(temps) == 10
            assert temps[0] == pytest.approx(20.0)
            assert temps[9] == pytest.approx(29.0)
        finally:
            cleanup_shared(shm)

    def test_compute_stats(self, readings: list[SensorReading]) -> None:
        shm, count = create_shared_temperatures(readings)
        try:
            stats = compute_stats_on_shared(shm.name, count)
            assert stats["mean"] == pytest.approx(24.5)
            assert stats["min"] == pytest.approx(20.0)
            assert stats["max"] == pytest.approx(29.0)
        finally:
            cleanup_shared(shm)

    def test_cleanup(self, readings: list[SensorReading]) -> None:
        shm, count = create_shared_temperatures(readings)
        name = shm.name
        cleanup_shared(shm)
        with pytest.raises(FileNotFoundError):
            from multiprocessing.shared_memory import SharedMemory
            SharedMemory(name=name, create=False)
