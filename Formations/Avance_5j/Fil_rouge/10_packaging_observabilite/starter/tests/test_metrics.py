"""Tests pour les metriques du pipeline."""

from pipeline.metrics import PipelineMetrics, format_report


class TestMetrics:
    def test_default_values(self) -> None:
        m = PipelineMetrics()
        assert m.files_read == 0
        assert m.readings_valid == 0

    def test_accumulate(self) -> None:
        m = PipelineMetrics()
        m.files_read = 10
        m.readings_valid = 500
        m.readings_invalid = 3
        m.total_duration_ms = 1234.5
        assert m.files_read == 10

    def test_format_report(self) -> None:
        m = PipelineMetrics(
            files_read=10,
            readings_valid=500,
            readings_invalid=3,
            total_duration_ms=1234.5,
            stage_durations_ms={"ingest": 500.0, "transform": 400.0, "write": 334.5},
        )
        report = format_report(m)
        assert "500" in report
        assert "ingest" in report
