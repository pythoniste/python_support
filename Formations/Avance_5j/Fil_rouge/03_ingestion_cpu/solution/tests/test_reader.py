"""Tests pour la lecture CSV et l'ecriture JSON."""

import json
from pathlib import Path

import pytest

from pipeline.models import SensorReading
from pipeline.reader import parse_csv, read_all_csv
from pipeline.writer import write_json


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
def csv_with_errors(tmp_path: Path) -> Path:
    p = tmp_path / "errors.csv"
    p.write_text(
        "sensor_id,temperature,humidity,pressure\n"
        "AB-1234,22.5,45.0,1013.25\n"
        "INVALIDE,999.0,45.0,1013.25\n"
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


class TestParseCsv:
    def test_valid_csv(self, csv_file: Path) -> None:
        readings = parse_csv(csv_file)
        assert len(readings) == 2
        assert readings[0].sensor_id == "AB-1234"

    def test_csv_with_errors_skips_invalid(self, csv_with_errors: Path) -> None:
        readings = parse_csv(csv_with_errors)
        assert len(readings) == 2


class TestReadAllCsv:
    def test_parallel_read(self, inbox_dir: Path) -> None:
        readings = read_all_csv(inbox_dir, max_workers=2)
        assert len(readings) == 5


class TestWriteJson:
    def test_write_and_read_back(self, tmp_path: Path) -> None:
        readings = [SensorReading("AB-1234", 22.5, 45.0, 1013.25)]
        out = tmp_path / "output.json"
        write_json(readings, out)
        data = json.loads(out.read_text())
        assert len(data) == 1
        assert data[0]["sensor_id"] == "AB-1234"
