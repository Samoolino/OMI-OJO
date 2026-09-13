"""Canonical production records.  Raw observations remain distinguishable from forecasts."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Literal

DataStatus = Literal["MEASURED", "FORECAST", "CALCULATED", "MODELLED", "ESTIMATED", "PROXY"]
BatchStatus = Literal[
    "CREATED", "COLLECTING", "HARVESTED", "ANALYSIS_PENDING", "QUALITY_REVIEW",
    "QUALITY_PASSED", "BATCH_LOCKED", "BOTTLED", "SEALED", "EVIDENCE_PACKAGED",
    "ANCHORED", "VERIFIED", "PUBLISHED", "QUARANTINED", "REJECTED"
]


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class Observation:
    variable: str
    value: float
    unit: str
    status: DataStatus
    source_id: str
    observed_at: datetime
    retrieved_at: datetime = field(default_factory=utcnow)
    confidence: float | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "variable": self.variable,
            "value": self.value,
            "unit": self.unit,
            "status": self.status,
            "source_id": self.source_id,
            "observed_at": self.observed_at.isoformat(),
            "retrieved_at": self.retrieved_at.isoformat(),
            "confidence": self.confidence,
        }


@dataclass
class RainfallEvent:
    event_id: str
    site_id: str
    forecast_mm: float | None = None
    observed_mm: float | None = None
    duration_minutes: int | None = None
    status: str = "FORECASTED"
    observations: list[Observation] = field(default_factory=list)


@dataclass
class CollectionPlan:
    event_id: str
    expected_gross_liters: float
    expected_usable_liters: float
    bag_capacity_liters: float
    safety_factor: float
    required_bags: int
    reserve_bags: int


@dataclass
class RainHarvestBatch:
    batch_id: str
    event_id: str
    site_id: str
    status: BatchStatus = "CREATED"
    collection_volume_liters: float = 0.0
    usable_volume_liters: float = 0.0
    premium_score: float | None = None
    premium_class: str | None = None
    evidence_root: str | None = None
    bottle_count: int = 0
    seal_ids: list[str] = field(default_factory=list)

    def lock(self) -> None:
        if self.status != "QUALITY_PASSED":
            raise ValueError("batch can only be locked after QUALITY_PASSED")
        self.status = "BATCH_LOCKED"
