from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from typing import Iterable


@dataclass(frozen=True)
class EvidenceManifestItem:
    artifact_id: str
    category: str
    reference: str
    status: str = "AVAILABLE"


@dataclass(frozen=True)
class S6BEvidenceManifest:
    milestone: str
    project_id: str
    release_state: str
    snapshot_id: str
    evidence_package_id: str
    configuration_revision: str
    items: tuple[EvidenceManifestItem, ...]
    deterministic_hash: str


def build_s6b_manifest(
    *,
    project_id: str,
    snapshot_id: str,
    evidence_package_id: str,
    release_state: str,
    configuration_revision: str,
    artifacts: Iterable[EvidenceManifestItem],
) -> S6BEvidenceManifest:
    ordered = tuple(sorted(artifacts, key=lambda item: (item.category, item.artifact_id)))
    canonical = {
        "milestone": "S6B",
        "project_id": project_id,
        "release_state": release_state,
        "snapshot_id": snapshot_id,
        "evidence_package_id": evidence_package_id,
        "configuration_revision": configuration_revision,
        "items": [asdict(item) for item in ordered],
    }
    digest = hashlib.sha256(
        json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return S6BEvidenceManifest(
        milestone="S6B",
        project_id=project_id,
        release_state=release_state,
        snapshot_id=snapshot_id,
        evidence_package_id=evidence_package_id,
        configuration_revision=configuration_revision,
        items=ordered,
        deterministic_hash=digest,
    )
