"""Plugin : moyenne glissante de la temperature."""

from __future__ import annotations

from pipeline.models import SensorReading
from pipeline.plugin_base import TransformPlugin


class MovingAveragePlugin(TransformPlugin):
    """Calcule la moyenne glissante de la temperature sur une fenetre configurable."""

    name = "moving_average"

    def __init__(self, window: int = 3) -> None:
        self.window = window

    def transform(self, readings: list[SensorReading]) -> list[SensorReading]:
        if len(readings) < self.window:
            return readings
        result: list[SensorReading] = []
        for i, reading in enumerate(readings):
            if i < self.window - 1:
                result.append(reading)
            else:
                window_temps = [
                    readings[j].temperature for j in range(i - self.window + 1, i + 1)
                ]
                avg = sum(window_temps) / self.window
                new_reading = SensorReading(
                    sensor_id=reading.sensor_id,
                    temperature=avg,
                    humidity=reading.humidity,
                    pressure=reading.pressure,
                )
                result.append(new_reading)
        return result
