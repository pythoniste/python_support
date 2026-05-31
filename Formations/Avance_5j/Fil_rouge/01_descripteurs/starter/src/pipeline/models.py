"""Modeles de donnees du pipeline.

A completer : implementer SensorReading avec les descripteurs.
"""

from __future__ import annotations

from pipeline.descriptors import RangeField, RegexField


class SensorReading:
    """Lecture d'un capteur IoT avec validation par descripteurs."""

    sensor_id = RegexField(r"[A-Z]{2}-\d{4}")
    temperature = RangeField(-40.0, 85.0)
    humidity = RangeField(0.0, 100.0)
    pressure = RangeField(300.0, 1100.0)

    def __init__(
        self,
        sensor_id: str,
        temperature: float,
        humidity: float,
        pressure: float,
    ) -> None:
        # TODO : affecter les quatre champs
        ...

    def __repr__(self) -> str:
        # TODO : retourner une representation lisible
        ...
