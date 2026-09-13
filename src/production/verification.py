"""Public verification rules for bottle/batch evidence."""
from dataclasses import dataclass


@dataclass(frozen=True)
class VerificationResult:
    identifier: str
    status: str
    evidence_root: str | None
    anchor_reference: str | None


def verify(identifier: str, evidence_root: str | None, anchor_reference: str | None) -> VerificationResult:
    if not identifier:
        raise ValueError("identifier required")
    status = "VERIFIED" if evidence_root and anchor_reference else "PENDING"
    return VerificationResult(identifier, status, evidence_root, anchor_reference)
