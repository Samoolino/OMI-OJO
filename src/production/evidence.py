"""Deterministic DMRV evidence manifest generation."""
from dataclasses import dataclass
from .provenance import sha256_hex


@dataclass(frozen=True)
class EvidencePackage:
    manifest: dict
    evidence_root: str


def build_evidence_package(records: dict[str, object], methodology_version: str) -> EvidencePackage:
    manifest = {
        "schema_version": "BE-EVIDENCE-0.1",
        "methodology_version": methodology_version,
        "records": records,
    }
    return EvidencePackage(manifest=manifest, evidence_root=sha256_hex(manifest))
