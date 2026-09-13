"""Blockchain proof adapter boundary. Raw telemetry is never written here."""
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class AnchorReceipt:
    network: str
    reference: str
    evidence_root: str
    status: str


class EvidenceAnchor(Protocol):
    def anchor(self, evidence_root: str) -> AnchorReceipt: ...


class DryRunAnchor:
    network = "DRY_RUN"

    def anchor(self, evidence_root: str) -> AnchorReceipt:
        if len(evidence_root) != 64:
            raise ValueError("evidence_root must be a SHA-256 hex digest")
        return AnchorReceipt(self.network, f"dryrun:{evidence_root[:16]}", evidence_root, "SIMULATED")
