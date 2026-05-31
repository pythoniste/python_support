"""Tests pour le pipeline avec backpressure."""

import asyncio
from pathlib import Path

import pytest

from pipeline.models import SensorReading
from pipeline.orchestrator import run_pipeline
from pipeline.stages import ingest_stage, transform_stage, write_stage


@pytest.fixture()
def inbox_with_data(tmp_path: Path) -> Path:
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    for i in range(3):
        (inbox / f"data_{i}.csv").write_text(
            "sensor_id,temperature,humidity,pressure\n"
            f"AB-{i:04d},{20.0 + i},50.0,1013.0\n"
        )
    return inbox


class TestStages:
    async def test_ingest_stage_sends_sentinel(self, inbox_with_data: Path) -> None:
        queue: asyncio.Queue[SensorReading | None] = asyncio.Queue(maxsize=10)
        await ingest_stage(inbox_with_data, queue)
        items: list[SensorReading | None] = []
        while not queue.empty():
            items.append(queue.get_nowait())
        assert items[-1] is None  # sentinelle
        assert len(items) == 4  # 3 lectures + 1 None

    async def test_write_stage_creates_output(self, tmp_path: Path) -> None:
        queue: asyncio.Queue[SensorReading | None] = asyncio.Queue(maxsize=10)
        await queue.put(SensorReading("AB-1234", 22.5, 45.0, 1013.25))
        await queue.put(None)
        outbox = tmp_path / "outbox"
        outbox.mkdir()
        await write_stage(queue, outbox)
        json_files = list(outbox.glob("*.json"))
        assert len(json_files) >= 1


class TestOrchestrator:
    async def test_run_pipeline_end_to_end(self, inbox_with_data: Path, tmp_path: Path) -> None:
        outbox = tmp_path / "outbox"
        outbox.mkdir()
        await run_pipeline(
            inbox=inbox_with_data,
            outbox=outbox,
            plugins=[],
            queue_size=5,
            timeout=10.0,
        )
        json_files = list(outbox.glob("*.json"))
        assert len(json_files) >= 1

    async def test_run_pipeline_timeout(self, tmp_path: Path) -> None:
        inbox = tmp_path / "inbox"
        inbox.mkdir()
        # Pas de fichiers -> le pipeline devrait terminer rapidement
        outbox = tmp_path / "outbox"
        outbox.mkdir()
        await run_pipeline(
            inbox=inbox, outbox=outbox, plugins=[], queue_size=5, timeout=2.0,
        )
