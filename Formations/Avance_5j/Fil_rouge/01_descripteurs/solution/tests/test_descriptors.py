"""Tests pour les descripteurs et le modele SensorReading."""

import pytest

from pipeline.descriptors import NonEmptyString, RangeField, RegexField, Validated
from pipeline.models import SensorReading


class TestRangeField:
    def test_valid_value(self) -> None:
        r = SensorReading("AB-1234", 22.5, 45.0, 1013.25)
        assert r.temperature == 22.5

    def test_value_at_min(self) -> None:
        r = SensorReading("AB-1234", -40.0, 0.0, 300.0)
        assert r.temperature == -40.0

    def test_value_at_max(self) -> None:
        r = SensorReading("AB-1234", 85.0, 100.0, 1100.0)
        assert r.temperature == 85.0

    def test_value_below_min(self) -> None:
        with pytest.raises(ValueError, match="hors de"):
            SensorReading("AB-1234", -50.0, 45.0, 1013.25)

    def test_value_above_max(self) -> None:
        with pytest.raises(ValueError, match="hors de"):
            SensorReading("AB-1234", 100.0, 45.0, 1013.25)

    def test_non_numeric_value(self) -> None:
        with pytest.raises((ValueError, TypeError)):
            SensorReading("AB-1234", "chaud", 45.0, 1013.25)  # type: ignore[arg-type]


class TestRegexField:
    def test_valid_sensor_id(self) -> None:
        r = SensorReading("AB-1234", 22.5, 45.0, 1013.25)
        assert r.sensor_id == "AB-1234"

    def test_invalid_sensor_id_lowercase(self) -> None:
        with pytest.raises(ValueError, match="matche pas"):
            SensorReading("ab-1234", 22.5, 45.0, 1013.25)

    def test_invalid_sensor_id_format(self) -> None:
        with pytest.raises(ValueError, match="matche pas"):
            SensorReading("ABC-123", 22.5, 45.0, 1013.25)

    def test_empty_sensor_id(self) -> None:
        with pytest.raises(ValueError):
            SensorReading("", 22.5, 45.0, 1013.25)


class TestNonEmptyString:
    def test_non_empty_string_accepts_valid(self) -> None:
        class Dummy:
            name = NonEmptyString()

        d = Dummy()
        d.name = "hello"
        assert d.name == "hello"

    def test_non_empty_string_rejects_empty(self) -> None:
        class Dummy:
            name = NonEmptyString()

        d = Dummy()
        with pytest.raises(ValueError, match="vide"):
            d.name = ""

    def test_non_empty_string_rejects_whitespace(self) -> None:
        class Dummy:
            name = NonEmptyString()

        d = Dummy()
        with pytest.raises(ValueError, match="vide"):
            d.name = "   "


class TestSensorReading:
    def test_repr(self) -> None:
        r = SensorReading("AB-1234", 22.5, 45.0, 1013.25)
        text = repr(r)
        assert "AB-1234" in text
        assert "22.5" in text

    def test_set_name_stores_in_instance_dict(self) -> None:
        r = SensorReading("AB-1234", 22.5, 45.0, 1013.25)
        assert "temperature" in r.__dict__

    def test_mutation_validates(self) -> None:
        r = SensorReading("AB-1234", 22.5, 45.0, 1013.25)
        r.temperature = 30.0
        assert r.temperature == 30.0
        with pytest.raises(ValueError):
            r.temperature = 200.0
