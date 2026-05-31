"""Metriques du pipeline."""

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

    def record_stage(self, name: str, duration_ms: float) -> None:
        """Enregistre la duree d'un etage."""
        self.stage_durations_ms[name] = duration_ms

    @property
    def readings_total(self) -> int:
        return self.readings_valid + self.readings_invalid

    @property
    def error_rate(self) -> float:
        if self.readings_total == 0:
            return 0.0
        return self.readings_invalid / self.readings_total


def format_report(metrics: PipelineMetrics) -> str:
    """Formatte un rapport lisible des metriques."""
    lines = [
        "=== Rapport du pipeline ===",
        f"Fichiers lus       : {metrics.files_read}",
        f"Lectures valides   : {metrics.readings_valid}",
        f"Lectures invalides : {metrics.readings_invalid}",
        f"Taux d'erreur      : {metrics.error_rate:.1%}",
        f"Duree totale       : {metrics.total_duration_ms:.1f} ms",
        "",
        "Duree par etage :",
    ]
    for name, duration in metrics.stage_durations_ms.items():
        lines.append(f"  {name:20s} : {duration:.1f} ms")
    return "\n".join(lines)
