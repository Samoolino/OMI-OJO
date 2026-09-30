"""QC and evidence-package processing for canonical Climate & ESG observations.

The evidence processor is downstream of source adapters and upstream of
reportability/release. It validates provenance, schema, time/location bounds,
source authorization, and evidence-class integrity without promoting evidence.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
import json
import math
from typing import Iterable, Mapping

from .reportable_data import Observation, ReportingRule, evaluate_reportability


class EvidenceQCState:
    QC_PASSED = "QC_PASSED"
    QUARANTINED = "QUARANTINED"
    SOURCE_UNAPPROVED = "SOURCE_UNAPPROVED"
    STALE = "STALE"
    OUT_OF_BOUNDARY = "OUT_OF_BOUNDARY"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class EvidenceQCDecision:
    observation_id: str
    state: str
    reasons: tuple[str, ...]


@dataclass(frozen=True)
class EvidencePackage:
    package_id: str
    schema_version: str
    created_at: datetime
    observation_ids: tuple[str, ...]
    source_ids: tuple[str, ...]
    evidence_classes: tuple[str, ...]
    qc_passed_ids: tuple[str, ...]
    quarantined_ids: tuple[str, ...]
    decision_ids: tuple[str, ...]
    methodology: tuple[str, ...]
    package_hash: str


def _canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _package_hash(payload: Mapping[str, object]) -> str:
    return sha256(_canonical_json(payload).encode("utf-8")).hexdigest()


def _metadata_complete(observation: Observation) -> bool:
    return {"provider", "source_snapshot_id", "methodology_status"}.issubset(observation.metadata)


def _finite_numeric_value(observation: Observation) -> bool:
    if isinstance(observation.value, str):
        return bool(observation.value.strip())
    return math.isfinite(float(observation.value))


def qc_observation(
    observation: Observation,
    *,
    approved_sources: frozenset[str],
    now: datetime | None = None,
    max_age_seconds: int = 172800,
    location: tuple[float, float] | None = None,
    spatial_tolerance_degrees: float = 0.05,
) -> EvidenceQCDecision:
    """Validate one observation without changing its evidence class."""
    if observation.source_id not in approved_sources:
        return EvidenceQCDecision(
            observation.observation_id,
            EvidenceQCState.SOURCE_UNAPPROVED,
            ("source_not_in_approved_source_set",),
        )

    if not _metadata_complete(observation):
        return EvidenceQCDecision(
            observation.observation_id,
            EvidenceQCState.QUARANTINED,
            ("required_provenance_metadata_missing",),
        )

    if not observation.unit.strip() or not _finite_numeric_value(observation):
        return EvidenceQCDecision(
            observation.observation_id,
            EvidenceQCState.REJECTED,
            ("invalid_unit_or_value",),
        )

    if observation.observed_at.tzinfo is None:
        return EvidenceQCDecision(
            observation.observation_id,
            EvidenceQCState.QUARANTINED,
            ("observation_timestamp_missing_timezone",),
        )

    current = now or datetime.now(timezone.utc)
    age = (current - observation.observed_at.astimezone(timezone.utc)).total_seconds()
    if age < 0 or age > max_age_seconds:
        return EvidenceQCDecision(
            observation.observation_id,
            EvidenceQCState.STALE,
            ("observation_outside_evidence_window",),
        )

    if not (-90 <= observation.location.latitude <= 90 and -180 <= observation.location.longitude <= 180):
        return EvidenceQCDecision(
            observation.observation_id,
            EvidenceQCState.OUT_OF_BOUNDARY,
            ("invalid_wgs84_coordinates",),
        )

    if location is not None:
        lat, lon = location
        if (
            abs(observation.location.latitude - lat) > spatial_tolerance_degrees
            or abs(observation.location.longitude - lon) > spatial_tolerance_degrees
        ):
            return EvidenceQCDecision(
                observation.observation_id,
                EvidenceQCState.OUT_OF_BOUNDARY,
                ("observation_outside_authorized_location_tolerance",),
            )

    return EvidenceQCDecision(
        observation.observation_id,
        EvidenceQCState.QC_PASSED,
        ("provenance_validated", "schema_validated", "time_validated", "location_validated"),
    )


def process_evidence(
    observations: Iterable[Observation],
    *,
    approved_sources: frozenset[str],
    now: datetime | None = None,
    max_age_seconds: int = 172800,
    location: tuple[float, float] | None = None,
    spatial_tolerance_degrees: float = 0.05,
) -> tuple[tuple[Observation, ...], tuple[EvidenceQCDecision, ...]]:
    """Return only QC-passed observations plus the complete decision ledger."""
    passed: list[Observation] = []
    decisions: list[EvidenceQCDecision] = []
    for observation in observations:
        decision = qc_observation(
            observation,
            approved_sources=approved_sources,
            now=now,
            max_age_seconds=max_age_seconds,
            location=location,
            spatial_tolerance_degrees=spatial_tolerance_degrees,
        )
        decisions.append(decision)
        if decision.state == EvidenceQCState.QC_PASSED:
            passed.append(observation)
    return tuple(passed), tuple(decisions)


def build_evidence_package(
    observations: Iterable[Observation],
    decisions: Iterable[EvidenceQCDecision],
    *,
    created_at: datetime | None = None,
    methodology: tuple[str, ...] = (
        "provider_provenance_checked",
        "schema_and_unit_checked",
        "timestamp_and_freshness_checked",
        "location_boundary_checked",
        "evidence_class_preserved",
    ),
) -> EvidencePackage:
    """Create a deterministic package manifest for an evidence-processing run."""
    observation_list = tuple(observations)
    decision_list = tuple(decisions)
    created = created_at or datetime.now(timezone.utc)
    if created.tzinfo is None:
        created = created.replace(tzinfo=timezone.utc)

    observation_ids = tuple(sorted(o.observation_id for o in observation_list))
    source_ids = tuple(sorted({o.source_id for o in observation_list}))
    evidence_classes = tuple(sorted({o.evidence_class.value for o in observation_list}))
    qc_passed_ids = tuple(sorted(d.observation_id for d in decision_list if d.state == EvidenceQCState.QC_PASSED))
    quarantined_ids = tuple(sorted(
        d.observation_id
        for d in decision_list
        if d.state in {
            EvidenceQCState.QUARANTINED,
            EvidenceQCState.SOURCE_UNAPPROVED,
            EvidenceQCState.STALE,
            EvidenceQCState.OUT_OF_BOUNDARY,
            EvidenceQCState.REJECTED,
        }
    ))
    decision_ids = tuple(sorted(d.observation_id for d in decision_list))

    payload = {
        "schema_version": "UB-02.EVIDENCE-PACKAGE.1",
        "observation_ids": observation_ids,
        "source_ids": source_ids,
        "evidence_classes": evidence_classes,
        "qc_passed_ids": qc_passed_ids,
        "quarantined_ids": quarantined_ids,
        "decision_ids": decision_ids,
        "methodology": methodology,
    }
    package_hash = _package_hash(payload)
    return EvidencePackage(
        package_id="EP-" + package_hash[:16],
        schema_version="UB-02.EVIDENCE-PACKAGE.1",
        created_at=created,
        observation_ids=observation_ids,
        source_ids=source_ids,
        evidence_classes=evidence_classes,
        qc_passed_ids=qc_passed_ids,
        quarantined_ids=quarantined_ids,
        decision_ids=decision_ids,
        methodology=methodology,
        package_hash=package_hash,
    )


def evaluate_qc_then_reportability(
    observations: Iterable[Observation],
    rules: Iterable[ReportingRule],
    *,
    approved_sources: frozenset[str],
    now: datetime | None = None,
) -> tuple[EvidencePackage, tuple[EvidenceQCDecision, ...], tuple]:
    """Enforce QC as the gate immediately before reportability evaluation."""
    observation_list = tuple(observations)
    rule_list = tuple(rules)
    passed, decisions = process_evidence(
        observation_list,
        approved_sources=approved_sources,
        now=now,
    )
    package = build_evidence_package(observation_list, decisions)
    rule_index = {(r.project_id, r.site_id, r.indicator_id): r for r in rule_list}
    reportability = tuple(
        evaluate_reportability(
            observation,
            rule_index[(observation.project_id, observation.site_id, observation.indicator_id)],
            now=now,
        )
        for observation in passed
        if (observation.project_id, observation.site_id, observation.indicator_id) in rule_index
    )
    return package, decisions, reportability
