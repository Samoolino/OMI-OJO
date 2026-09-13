"""Environmental/water fingerprint and release gates.

This module records provenance and does not claim regulatory potability by itself.
"""
from dataclasses import dataclass, field
from typing import Literal

MeasurementStatus = Literal["MEASURED", "CALCULATED", "MODELLED", "ESTIMATED", "PROXY"]


@dataclass(frozen=True)
class Measurement:
    parameter: str
    value: float
    unit: str
    status: MeasurementStatus
    source_id: str
    method: str
    timestamp: str


@dataclass
class QualityProfile:
    environmental: list[Measurement] = field(default_factory=list)
    water: list[Measurement] = field(default_factory=list)
    passed: bool = False
    rejection_reasons: list[str] = field(default_factory=list)

    def evaluate(self, required_parameters: set[str]) -> bool:
        measured = {m.parameter for m in self.water if m.status == "MEASURED"}
        missing = sorted(required_parameters - measured)
        self.rejection_reasons = [f"missing measured parameter: {x}" for x in missing]
        self.passed = not self.rejection_reasons
        return self.passed
