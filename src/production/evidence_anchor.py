"""S6A deterministic evidence-anchor registry and verification primitives.

The module is chain-agnostic: it creates the exact record that an anchor
adapter/contract must persist. It never treats an anchor as environmental truth.
"""
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any
from .provenance import canonical_json, sha256_hex


ANCHOR_STATUSES = {"PENDING", "ANCHORED", "MISMATCHED", "NOT_FOUND", "SUPERSEDED", "HOLD"}


@dataclass(frozen=True)
class AnchorRecord:
    evidence_id: str
    schema_version: str
    evidence_root: str
    network_id: str
    chain_id: int
    contract_address: str
    transaction_hash: str
    block_number: int
    block_timestamp: str
    anchor_status: str
    anchored_at: str
    verifier_version: str = "S6A-1.0"

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def canonical_evidence_package(
    *,
    evidence_id: str,
    project_id: str,
    evidence_class: str,
    source_refs: list[str],
    observation_refs: list[str],
    event_site_refs: list[str],
    methodology_ref: str,
    quality_state: str,
    created_at: str,
    observation_window: dict[str, str] | None,
    geography_ref: str,
    content_hashes: list[str],
    parent_evidence: list[str] | None = None,
    status: str = "REPORTABLE",
    schema_version: str = "BE-EVIDENCE-1.0",
) -> dict[str, Any]:
    if not evidence_id or not project_id:
        raise ValueError("evidence_id and project_id are required")
    if not source_refs:
        raise ValueError("at least one source reference is required")
    package = {
        "content_hashes": sorted(content_hashes),
        "created_at": created_at,
        "evidence_class": evidence_class,
        "evidence_id": evidence_id,
        "event_site_refs": sorted(event_site_refs),
        "geography_ref": geography_ref,
        "methodology_ref": methodology_ref,
        "observation_refs": sorted(observation_refs),
        "observation_window": observation_window or {},
        "parent_evidence": sorted(parent_evidence or []),
        "project_id": project_id,
        "quality_state": quality_state,
        "schema_version": schema_version,
        "source_refs": sorted(source_refs),
        "status": status,
    }
    return package


def evidence_root(package: dict[str, Any]) -> str:
    """Return a deterministic SHA-256 root for a canonical package."""
    return sha256_hex(package)


def package_bytes(package: dict[str, Any]) -> bytes:
    return canonical_json(package)


def validate_anchor_record(record: AnchorRecord) -> None:
    if record.anchor_status not in ANCHOR_STATUSES:
        raise ValueError(f"unsupported anchor status: {record.anchor_status}")
    if len(record.evidence_root) != 64:
        raise ValueError("evidence_root must be a SHA-256 hex digest")
    try:
        int(record.evidence_root, 16)
    except ValueError as exc:
        raise ValueError("evidence_root must be hexadecimal") from exc
    if record.chain_id <= 0:
        raise ValueError("chain_id must be positive")
    if not record.evidence_id:
        raise ValueError("evidence_id is required")


def verification_status(package: dict[str, Any], anchored_root: str) -> str:
    """Compare reconstructed package root with an externally supplied anchor."""
    if not anchored_root:
        return "NOT_FOUND"
    calculated = evidence_root(package)
    return "MATCHED" if calculated == anchored_root.lower() else "MISMATCHED"


def now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
