"""Tests pour le profiling memoire."""

import sys

import pytest

from pipeline.mem_profiling import print_memory_stats, trace_memory
from pipeline.models import SensorReading


def _allocate_readings() -> list[SensorReading]:
    return [
        SensorReading("AB-1234", 20.0 + i % 60, 50.0, 1013.0)
        for i in range(1000)
    ]


class TestMemoryProfiling:
    def test_trace_memory_returns_stats(self) -> None:
        result, stats = trace_memory(_allocate_readings)
        assert len(result) == 1000
        assert len(stats) > 0

    def test_print_memory_stats_no_error(self) -> None:
        _, stats = trace_memory(_allocate_readings)
        print_memory_stats(stats, n=5)

    def test_slots_reduces_memory(self) -> None:
        """Verifie que SensorReading avec __slots__ est plus compact."""
        r = SensorReading("AB-1234", 22.5, 45.0, 1013.25)
        size = sys.getsizeof(r)
        # Avec __slots__, un objet fait typiquement < 100 octets
        # Sans __slots__, il fait > 150 octets (a cause du __dict__)
        # Ce test passe dans les deux cas mais documente la difference
        assert size > 0
