"""Tests pour le systeme de plugins."""

import pytest

from pipeline.models import SensorReading
from pipeline.plugin_base import TransformPlugin

# Force l'import des plugins pour les enregistrer
import pipeline.plugins  # noqa: F401


def _make_readings(n: int = 5) -> list[SensorReading]:
    """Cree une liste de lectures de test."""
    return [
        SensorReading("AB-1234", 20.0 + i, 50.0, 1013.0)
        for i in range(n)
    ]


class TestPluginRegistry:
    def test_list_plugins_not_empty(self) -> None:
        names = TransformPlugin.list_plugins()
        assert len(names) >= 3

    def test_get_plugin_moving_average(self) -> None:
        cls = TransformPlugin.get_plugin("moving_average")
        assert cls is not None

    def test_get_plugin_unknown_raises(self) -> None:
        with pytest.raises(KeyError):
            TransformPlugin.get_plugin("inexistant")

    def test_duplicate_name_raises(self) -> None:
        with pytest.raises(ValueError, match="existe deja"):
            class BadPlugin(TransformPlugin):
                name = "moving_average"

                def transform(self, readings: list[SensorReading]) -> list[SensorReading]:
                    return readings


class TestMovingAverage:
    def test_basic(self) -> None:
        plugin = TransformPlugin.get_plugin("moving_average")(window=3)
        readings = _make_readings(5)
        result = plugin.transform(readings)
        assert len(result) > 0
        # La moyenne glissante de [20, 21, 22, 23, 24] fenetre 3 :
        # premier element transforme devrait refleter la moyenne
        assert result[2].temperature == pytest.approx(21.0, abs=0.1)


class TestAnomalyDetector:
    def test_no_anomaly_in_uniform_data(self) -> None:
        plugin = TransformPlugin.get_plugin("anomaly_detector")(threshold_std=2.0)
        readings = _make_readings(10)
        result = plugin.transform(readings)
        anomalies = [r for r in result if getattr(r, "is_anomaly", False)]
        # Avec des valeurs progressives proches, peu ou pas d'anomalies
        assert len(anomalies) <= 2


class TestUnitConverter:
    def test_conversion(self) -> None:
        plugin = TransformPlugin.get_plugin("unit_converter")()
        readings = [SensorReading("AB-1234", 0.0, 50.0, 1013.0)]
        result = plugin.transform(readings)
        # 0 C = 32 F — mais la temperature est validee par RangeField
        # Le plugin doit adapter les bornes ou travailler sur une copie
        assert result[0].temperature == pytest.approx(32.0, abs=0.1)
