"""Claim-to-evidence graph for reporting, grant and VDR traceability."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import hashlib
import json
from typing import Iterable


class ClaimState(StrEnum):
    DRAFT = "DRAFT"
    SUPPORTED = "SUPPORTED"
    BLOCKED = "BLOCKED"
    RELEASED = "RELEASED"


@dataclass(frozen=True)
class EvidenceLink:
    claim_id: str
    observation_ids: tuple[str, ...]
    evidence_package_id: str
    snapshot_id: str
    methodology_version: str
    source_ids: tuple[str, ...]


@dataclass(frozen=True)
class Claim:
    claim_id: str
    project_id: str
    statement: str
    indicator_id: str
    state: ClaimState
    evidence: EvidenceLink
    deterministic_hash: str


def build_claim(
    *,
    project_id: str,
    statement: str,
    indicator_id: str,
    observation_ids: Iterable[str],
    evidence_package_id: str,
    snapshot_id: str,
    methodology_version: str,
    source_ids: Iterable[str],
    state: ClaimState = ClaimState.DRAFT,
) -> Claim:
    evidence = EvidenceLink(
        claim_id="PENDING",
        observation_ids=tuple(sorted(observation_ids)),
        evidence_package_id=evidence_package_id,
        snapshot_id=snapshot_id,
        methodology_version=methodology_version,
        source_ids=tuple(sorted(source_ids)),
    )
    canonical = {
        "project_id": project_id,
        "statement": statement,
        "indicator_id": indicator_id,
        "state": state.value,
        "observation_ids": evidence.observation_ids,
        "evidence_package_id": evidence_package_id,
        "snapshot_id": snapshot_id,
        "methodology_version": methodology_version,
        "source_ids": evidence.source_ids,
    }
    digest = hashlib.sha256(json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    claim_id = f"CLM-{digest[:16]}"
    evidence = EvidenceLink(claim_id=claim_id, **{k: getattr(evidence, k) for k in evidence.__dataclass_fields__ if k != "claim_id"})
    return Claim(claim_id, project_id, statement, indicator_id, state, evidence, digest)
