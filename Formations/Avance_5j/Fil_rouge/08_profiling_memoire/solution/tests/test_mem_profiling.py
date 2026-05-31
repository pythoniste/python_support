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
