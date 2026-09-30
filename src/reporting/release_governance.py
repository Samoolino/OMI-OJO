"""Governed reporting release state machine.

Release governance never changes evidence class or environmental truth. It only
controls whether an immutable reporting snapshot may move through institutional
publication states.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
import hashlib
import json


class ReleaseState(StrEnum):
    DRAFT = "DRAFT"
    REVIEW = "REVIEW"
    RETURNED = "RETURNED"
    BLOCKED = "BLOCKED"
    APPROVED = "APPROVED"
    RELEASED = "RELEASED"
    REJECTED = "REJECTED"
    QUARANTINED = "QUARANTINED"
    SUPERSEDED = "SUPERSEDED"


@dataclass(frozen=True)
class ReleaseDecision:
    release_id: str
    snapshot_id: str
    evidence_package_id: str
    snapshot_hash: str
    configuration_revision: str
    policy_revision: str
    state: ReleaseState
    reviewer: str | None
    reason: str | None
    decided_at: str
    deterministic_hash: str


def _hash(payload: dict[str, object]) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def create_release(
    *,
    snapshot_id: str,
    evidence_package_id: str,
    snapshot_hash: str,
    configuration_revision: str,
    policy_revision: str,
) -> ReleaseDecision:
    payload = {
        "snapshot_id": snapshot_id,
        "evidence_package_id": evidence_package_id,
        "snapshot_hash": snapshot_hash,
        "configuration_revision": configuration_revision,
        "policy_revision": policy_revision,
        "state": ReleaseState.DRAFT.value,
    }
    digest = _hash(payload)
    return ReleaseDecision(
        release_id=f"REL-{digest[:16]}",
        snapshot_id=snapshot_id,
        evidence_package_id=evidence_package_id,
        snapshot_hash=snapshot_hash,
        configuration_revision=configuration_revision,
        policy_revision=policy_revision,
        state=ReleaseState.DRAFT,
        reviewer=None,
        reason=None,
        decided_at=datetime.now(timezone.utc).isoformat(),
        deterministic_hash=digest,
    )


_ALLOWED: dict[ReleaseState, frozenset[ReleaseState]] = {
    ReleaseState.DRAFT: frozenset({ReleaseState.REVIEW, ReleaseState.QUARANTINED}),
    ReleaseState.REVIEW: frozenset({ReleaseState.APPROVED, ReleaseState.RETURNED, ReleaseState.BLOCKED, ReleaseState.REJECTED}),
    ReleaseState.RETURNED: frozenset({ReleaseState.REVIEW, ReleaseState.QUARANTINED}),
    ReleaseState.BLOCKED: frozenset({ReleaseState.REVIEW, ReleaseState.REJECTED}),
    ReleaseState.APPROVED: frozenset({ReleaseState.RELEASED, ReleaseState.SUPERSEDED}),
    ReleaseState.RELEASED: frozenset({ReleaseState.SUPERSEDED}),
    ReleaseState.REJECTED: frozenset(),
    ReleaseState.QUARANTINED: frozenset({ReleaseState.REVIEW, ReleaseState.REJECTED}),
    ReleaseState.SUPERSEDED: frozenset(),
}


def transition_release(
    release: ReleaseDecision,
    target: ReleaseState,
    *,
    reviewer: str | None = None,
    reason: str | None = None,
) -> ReleaseDecision:
    if target not in _ALLOWED[release.state]:
        raise ValueError(f"invalid release transition: {release.state} -> {target}")
    if target in {ReleaseState.APPROVED, ReleaseState.REJECTED, ReleaseState.BLOCKED, ReleaseState.RELEASED} and not reviewer:
        raise ValueError(f"reviewer is required for {target}")
    if target in {ReleaseState.RETURNED, ReleaseState.BLOCKED, ReleaseState.REJECTED, ReleaseState.QUARANTINED} and not reason:
        raise ValueError(f"reason is required for {target}")
    payload = {
        "release_id": release.release_id,
        "snapshot_id": release.snapshot_id,
        "evidence_package_id": release.evidence_package_id,
        "snapshot_hash": release.snapshot_hash,
        "configuration_revision": release.configuration_revision,
        "policy_revision": release.policy_revision,
        "state": target.value,
        "reviewer": reviewer,
        "reason": reason,
    }
    digest = _hash(payload)
    return ReleaseDecision(
        release_id=release.release_id,
        snapshot_id=release.snapshot_id,
        evidence_package_id=release.evidence_package_id,
        snapshot_hash=release.snapshot_hash,
        configuration_revision=release.configuration_revision,
        policy_revision=release.policy_revision,
        state=target,
        reviewer=reviewer,
        reason=reason,
        decided_at=datetime.now(timezone.utc).isoformat(),
        deterministic_hash=digest,
    )
