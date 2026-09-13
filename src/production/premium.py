"""Versioned premium-harvest classification framework."""
from dataclasses import dataclass


@dataclass(frozen=True)
class PremiumAssessment:
    score: float
    classification: str
    methodology_version: str
    confidence: float | None


def assess(
    *,
    first_flush_passed: bool,
    quality_passed: bool,
    provenance_complete: bool,
    environmental_complete: bool,
    methodology_version: str = "PHM-0.1",
) -> PremiumAssessment:
    checks = [first_flush_passed, quality_passed, provenance_complete, environmental_complete]
    score = sum(25.0 for value in checks if value)
    classification = "CLASS_A" if score == 100 else "CLASS_B" if score >= 75 else "QUARANTINED"
    return PremiumAssessment(score, classification, methodology_version, None)
