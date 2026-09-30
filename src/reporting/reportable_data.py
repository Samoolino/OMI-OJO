"""Canonical reportability engine for OMI-OJO Climate & ESG reporting.

This module deliberately separates source availability from reportability. Remote
and modelled data can provide contextual evidence, but a project may require a
measured or verified class before an indicator becomes reportable.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from math import hypot
from typing import Iterable


class EvidenceClass(str, Enum):
    CONTEXTUAL = "CONTEXTUAL"
    MODELED = "MODELED"
    SATELLITE = "SATELLITE"
    MEASURED = "MEASURED"
    VERIFIED_MEASUREMENT = "VERIFIED_MEASUREMENT"


class ReportabilityState(str, Enum):
    DISCOVERED = "DISCOVERED"
    INGESTED = "INGESTED"
    LOCATION_MATCHED = "LOCATION_MATCHED"
    TIME_MATCHED = "TIME_MATCHED"
    QC_PASSED = "QC_PASSED"
    RECONCILED = "RECONCILED"
    REPORTABLE = "REPORTABLE"
    CONTEXTUAL_ONLY = "CONTEXTUAL_ONLY"
    SOURCE_UNAPPROVED = "SOURCE_UNAPPROVED"
    STALE = "STALE"
    OUT_OF_BOUNDARY = "OUT_OF_BOUNDARY"
    QUARANTINED = "QUARANTINED"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class Location:
    latitude: float
    longitude: float


@dataclass(frozen=True)
class Observation:
    observation_id: str
    project_id: str
    site_id: str
    indicator_id: str
    observed_at: datetime
    location: Location
    value: float | str
    unit: str
    source_id: str
    evidence_class: EvidenceClass
    qc_passed: bool = False
    reconciled: bool = False
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class ReportingRule:
    project_id: str
    site_id: str
    indicator_id: str
    allowed_sources: frozenset[str]
    minimum_evidence_class: EvidenceClass
    location: Location
    spatial_tolerance_degrees: float
    max_age_seconds: int
    require_qc: bool = True
    require_reconciliation: bool = False


@dataclass(frozen=True)
class ReportabilityDecision:
    observation_id: str
    state: ReportabilityState
    reasons: tuple[str, ...]


def _evidence_rank(kind: EvidenceClass) -> int:
    return {
        EvidenceClass.CONTEXTUAL: 1,
        EvidenceClass.MODELED: 2,
        EvidenceClass.SATELLITE: 3,
        EvidenceClass.MEASURED: 4,
        EvidenceClass.VERIFIED_MEASUREMENT: 5,
    }[kind]


def _distance(a: Location, b: Location) -> float:
    return hypot(a.latitude - b.latitude, a.longitude - b.longitude)


def evaluate_reportability(
    observation: Observation,
    rule: ReportingRule,
    *,
    now: datetime | None = None,
) -> ReportabilityDecision:
    """Evaluate one observation against the project's reporting contract."""
    reasons: list[str] = []

    if observation.project_id != rule.project_id or observation.site_id != rule.site_id:
        return ReportabilityDecision(observation.observation_id, ReportabilityState.OUT_OF_BOUNDARY, ("project_or_site_mismatch",))
    if observation.indicator_id != rule.indicator_id:
        return ReportabilityDecision(observation.observation_id, ReportabilityState.REJECTED, ("indicator_mismatch",))
    if observation.source_id not in rule.allowed_sources:
        return ReportabilityDecision(observation.observation_id, ReportabilityState.SOURCE_UNAPPROVED, ("source_not_approved_for_project",))

    distance = _distance(observation.location, rule.location)
    if distance > rule.spatial_tolerance_degrees:
        return ReportabilityDecision(observation.observation_id, ReportabilityState.OUT_OF_BOUNDARY, ("location_outside_project_tolerance",))
    reasons.append("location_matched")

    current = now or datetime.now(timezone.utc)
    observed = observation.observed_at
    if observed.tzinfo is None:
        observed = observed.replace(tzinfo=timezone.utc)
    age = (current - observed).total_seconds()
    if age < 0 or age > rule.max_age_seconds:
        return ReportabilityDecision(observation.observation_id, ReportabilityState.STALE, ("observation_outside_reporting_window",))
    reasons.append("time_matched")

    if rule.require_qc and not observation.qc_passed:
        return ReportabilityDecision(observation.observation_id, ReportabilityState.QUARANTINED, ("qc_required",))
    reasons.append("qc_passed")

    if _evidence_rank(observation.evidence_class) < _evidence_rank(rule.minimum_evidence_class):
        return ReportabilityDecision(observation.observation_id, ReportabilityState.CONTEXTUAL_ONLY, ("evidence_class_below_project_requirement",))

    if rule.require_reconciliation and not observation.reconciled:
        return ReportabilityDecision(observation.observation_id, ReportabilityState.QC_PASSED, ("reconciliation_required",))
    if rule.require_reconciliation:
        reasons.append("reconciled")

    return ReportabilityDecision(observation.observation_id, ReportabilityState.REPORTABLE, tuple(reasons))


def evaluate_batch(
    observations: Iterable[Observation],
    rules: Iterable[ReportingRule],
    *,
    now: datetime | None = None,
) -> list[ReportabilityDecision]:
    """Evaluate observations using the matching project/site/indicator rule."""
    rule_index = {(r.project_id, r.site_id, r.indicator_id): r for r in rules}
    decisions: list[ReportabilityDecision] = []
    for observation in observations:
        rule = rule_index.get((observation.project_id, observation.site_id, observation.indicator_id))
        if rule is None:
            decisions.append(ReportabilityDecision(observation.observation_id, ReportabilityState.SOURCE_UNAPPROVED, ("no_reporting_rule",)))
            continue
        decisions.append(evaluate_reportability(observation, rule, now=now))
    return decisions
