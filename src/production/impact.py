"""Traceable ESG/GHG calculations; claims remain methodology-gated."""
from dataclasses import dataclass
from typing import Literal

DataBasis = Literal["MEASURED", "CALCULATED", "MODELLED", "ESTIMATED", "PROXY"]


@dataclass(frozen=True)
class ImpactMetric:
    metric_id: str
    value: float
    unit: str
    basis: DataBasis
    methodology_version: str
    source_id: str
    status: str = "DRAFT"


def calculate_emissions(activity: float, emission_factor: float) -> float:
    if activity < 0 or emission_factor < 0:
        raise ValueError("activity and emission factor must be non-negative")
    return activity * emission_factor
