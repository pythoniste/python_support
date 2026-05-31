"""Plugin : detection d'anomalies de temperature.

A completer.
"""

from __future__ import annotations

from pipeline.models import SensorReading
from pipeline.plugin_base import TransformPlugin


# TODO : implementer AnomalyDetectorPlugin
# - name = "anomaly_detector"
# - __init__(self, threshold_std: float = 2.0)
# - transform : marque les lectures anormales (ajoute un attribut `is_anomaly`)
