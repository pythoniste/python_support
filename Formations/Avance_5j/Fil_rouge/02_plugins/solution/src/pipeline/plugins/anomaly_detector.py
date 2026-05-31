"""Plugin : detection d'anomalies de temperature."""

from __future__ import annotations

import statistics

from pipeline.models import SensorReading
from pipeline.plugin_base import TransformPlugin


class AnomalyDetectorPlugin(TransformPlugin):
    """Marque les lectures dont la temperature s'ecarte de plus de N ecarts-types."""

    name = "anomaly_detector"

    def __init__(self, threshold_std: float = 2.0) -> None:
        self.threshold_std = threshold_std

    def transform(self, readings: list[SensorReading]) -> list[SensorReading]:
        if len(readings) < 2:
            return readings
        temps = [r.temperature for r in readings]
        mean = statistics.mean(temps)
        std = statistics.stdev(temps)
        if std == 0:
            return readings
        for reading in readings:
            z_score = abs(reading.temperature - mean) / std
            reading.is_anomaly = z_score > self.threshold_std  # type: ignore[attr-defined]
        return readings
