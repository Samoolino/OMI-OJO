"""Forecast/observation reconciliation without collapsing provenance."""
from dataclasses import dataclass


@dataclass(frozen=True)
class RainfallReconciliation:
    predicted_mm: float
    actual_mm: float

    @property
    def absolute_error_mm(self) -> float:
        return abs(self.predicted_mm - self.actual_mm)

    @property
    def percentage_error(self) -> float | None:
        if self.actual_mm == 0:
            return None if self.predicted_mm else 0.0
        return self.absolute_error_mm / self.actual_mm * 100


def reconcile(predicted_mm: float, actual_mm: float) -> RainfallReconciliation:
    if predicted_mm < 0 or actual_mm < 0:
        raise ValueError("rainfall cannot be negative")
    return RainfallReconciliation(predicted_mm, actual_mm)


def accuracy_score_percent(predicted_mm: float, actual_mm: float) -> float:
    result = reconcile(predicted_mm, actual_mm)
    if actual_mm == 0:
        return 100.0 if predicted_mm == 0 else 0.0
    return max(0.0, 100.0 - result.percentage_error)
