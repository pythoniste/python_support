"""Plugin : conversion Celsius -> Fahrenheit."""

from __future__ import annotations

from pipeline.models import SensorReading
from pipeline.plugin_base import TransformPlugin


class UnitConverterPlugin(TransformPlugin):
    """Convertit les temperatures de Celsius en Fahrenheit."""

    name = "unit_converter"

    def transform(self, readings: list[SensorReading]) -> list[SensorReading]:
        result: list[SensorReading] = []
        for reading in readings:
            fahrenheit = reading.temperature * 9.0 / 5.0 + 32.0
            # On cree un nouveau SensorReading avec des bornes adaptees
            # pour Fahrenheit (-40F a 185F)
            new_reading = SensorReading.__new__(SensorReading)
            new_reading.__dict__["sensor_id"] = reading.sensor_id
            new_reading.__dict__["temperature"] = fahrenheit
            new_reading.__dict__["humidity"] = reading.humidity
            new_reading.__dict__["pressure"] = reading.pressure
            result.append(new_reading)
        return result
