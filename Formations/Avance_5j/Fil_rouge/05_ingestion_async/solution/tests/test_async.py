"""Tests pour la lecture et ecriture asynchrones."""

import json
from pathlib import Path

import pytest

from pipeline.async_reader import parse_csv_async, read_all_csv_async
from pipeline.async_writer import write_json_async
from pipeline.models import SensorReading


@pytest.fixture()
def csv_file(tmp_path: Path) -> Path:
    p = tmp_path / "test.csv"
    p.write_text(
        "sensor_id,temperature,humidity,pressure\n"
        "AB-1234,22.5,45.0,1013.25\n"
        "CD-5678,18.3,55.0,1012.00\n"
    )
    return p


@pytest.fixture()
def inbox_dir(tmp_path: Path) -> Path:
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    for i in range(5):
        (inbox / f"data_{i}.csv").write_text(
            "sensor_id,temperature,humidity,pressure\n"
            f"AB-{i:04d},{20.0 + i},50.0,1013.0\n"
        )
    return inbox


class TestAsyncReader:
    async def test_parse_csv_async(self, csv_file: Path) -> None:
        readings = await parse_csv_async(csv_file)
        assert len(readings) == 2
        assert readings[0].sensor_id == "AB-1234"

    async def test_read_all_csv_async(self, inbox_dir: Path) -> None:
        readings = await read_all_csv_async(inbox_dir)
        assert len(readings) == 5


class TestAsyncWriter:
    async def test_write_json_async(self, tmp_path: Path) -> None:
        readings = [SensorReading("AB-1234", 22.5, 45.0, 1013.25)]
        out = tmp_path / "output.json"
        await write_json_async(readings, out)
        data = json.loads(out.read_text())
        assert len(data) == 1
        assert data[0]["sensor_id"] == "AB-1234"
