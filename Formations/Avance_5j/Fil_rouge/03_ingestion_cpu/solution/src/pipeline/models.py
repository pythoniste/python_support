"""Modeles de donnees du pipeline."""

from __future__ import annotations

from pipeline.descriptors import RangeField, RegexField


class SensorReading:
    sensor_id = RegexField(r"[A-Z]{2}-\d{4}")
    temperature = RangeField(-40.0, 85.0)
    humidity = RangeField(0.0, 100.0)
    pressure = RangeField(300.0, 1100.0)

    def __init__(self, sensor_id: str, temperature: float, humidity: float, pressure: float) -> None:
        self.sensor_id = sensor_id
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure

    def __repr__(self) -> str:
        return (
            f"SensorReading(sensor_id={self.sensor_id!r}, "
            f"temperature={self.temperature}, humidity={self.humidity}, "
            f"pressure={self.pressure})"
        )
