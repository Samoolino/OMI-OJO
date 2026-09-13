"""Empirical forecast-versus-measured rainfall reconciliation.

Forecast snapshots and measured telemetry remain separate evidence records. This
module only reconciles them; it never promotes forecast data to measured data.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from .ingestion import Observation, ForecastSnapshot
from .rainfall import RainfallReconciliation, reconcile


@dataclass(frozen=True)
class RainfallComparison:
    forecast_snapshot_id: str
    observation_id: str
    forecast_mm: float
    measured_mm: float
    comparison: RainfallReconciliation
    matched_at: datetime

    @property
    def accuracy_percent(self) -> float:
        if self.measured_mm == 0:
            return 100.0 if self.forecast_mm == 0 else 0.0
        return max(0.0, 100.0 - self.comparison.percentage_error)


def compare_forecast_to_measurement(
    snapshot: ForecastSnapshot,
    observation: Observation,
    *,
    rainfall_variable: str = "precipitation",
) -> RainfallComparison:
    if observation.variable != rainfall_variable:
        raise ValueError("observation is not the configured rainfall variable")
    if observation.status != "MEASURED":
        raise ValueError("forecast reconciliation requires a MEASURED observation")
    forecast_value = snapshot.payload.get(rainfall_variable)
    if not isinstance(forecast_value, (int, float)):
        raise ValueError("forecast snapshot has no numeric rainfall value")
    comparison = reconcile(float(forecast_value), observation.value)
    return RainfallComparison(
        forecast_snapshot_id=snapshot.snapshot_id,
        observation_id=observation.observation_id,
        forecast_mm=float(forecast_value),
        measured_mm=observation.value,
        comparison=comparison,
        matched_at=observation.observed_at,
    )


def summarize_accuracy(comparisons: Iterable[RainfallComparison]) -> dict[str, float | int]:
    rows = list(comparisons)
    if not rows:
        return {"sample_count": 0, "mean_accuracy_percent": 0.0, "mean_absolute_error_mm": 0.0}
    return {
        "sample_count": len(rows),
        "mean_accuracy_percent": sum(r.accuracy_percent for r in rows) / len(rows),
        "mean_absolute_error_mm": sum(r.comparison.absolute_error_mm for r in rows) / len(rows),
    }
