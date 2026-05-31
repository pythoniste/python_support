"""Metriques du pipeline.

A completer : implementer PipelineMetrics et format_report.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PipelineMetrics:
    """Accumule les metriques du pipeline."""

    files_read: int = 0
    readings_valid: int = 0
    readings_invalid: int = 0
    total_duration_ms: float = 0.0
    stage_durations_ms: dict[str, float] = field(default_factory=dict)

    # TODO : ajouter des methodes pour enregistrer les metriques


def format_report(metrics: PipelineMetrics) -> str:
    """Formatte un rapport lisible des metriques."""
    # TODO : construire un rapport texte
    ...
