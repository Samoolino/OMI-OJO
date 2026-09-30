"""Canonical governed refresh pipeline.

Refresh now enforces:
collection → QC/evidence package → reportability → DRAFT snapshot → persistence.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable, Iterable

from .agentic_collection import CollectionRun, process_collection_evidence
from .engagement_orchestrator import OrchestrationPlan, ingest_plan
from .observation_store import ObservationStore
from .refresh_policy import RefreshPolicy, next_refresh
from .reportable_data import Observation, ReportingRule, evaluate_batch
from .reporting_snapshot import build_snapshot
from .snapshot_store import SnapshotStore


@dataclass(frozen=True)
class RefreshResult:
    engagement_id: str
    project_id: str
    report_family: str
    ingested: int
    decisions: int
    snapshot_id: str
    snapshot_hash: str
    next_refresh_at: str | None
    evidence_package_id: str | None = None
    qc_decisions: int = 0


def run_refresh(
    *,
    policy: RefreshPolicy,
    project_id: str,
    report_family: str,
    period_start: datetime,
    period_end: datetime,
    observations: Iterable[Observation],
    rules: Iterable[ReportingRule],
    observation_store: ObservationStore,
    snapshot_store: SnapshotStore,
    now: datetime | None = None,
    approved_sources: frozenset[str] | None = None,
    evidence_location: tuple[float, float] | None = None,
) -> RefreshResult:
    current = now or datetime.now(timezone.utc)
    items = tuple(observations)
    rule_list = tuple(rules)
    approved = approved_sources or frozenset(
        source for rule in rule_list for source in rule.allowed_sources
    )

    evidence_run = process_collection_evidence(
        collection=CollectionRun(actions=tuple(), observations=items, skipped=tuple()),
        approved_sources=approved,
        now=current,
        location=evidence_location,
    )
    reportability = evaluate_batch(evidence_run.reportable_observations, rule_list, now=current)

    persisted = observation_store.upsert(evidence_run.reportable_observations)
    snapshot = build_snapshot(
        project_id=project_id,
        report_family=report_family,
        period_start=period_start,
        period_end=period_end,
        observations=evidence_run.reportable_observations,
        decisions=reportability,
        release_state="DRAFT",
    )
    snapshot_store.save(snapshot)

    scheduled = next_refresh(current, policy)
    return RefreshResult(
        engagement_id=policy.engagement_id,
        project_id=project_id,
        report_family=report_family,
        ingested=persisted,
        decisions=len(reportability),
        snapshot_id=snapshot.snapshot_id,
        snapshot_hash=snapshot.deterministic_hash,
        next_refresh_at=scheduled.isoformat() if scheduled else None,
        evidence_package_id=evidence_run.package.package_id,
        qc_decisions=len(evidence_run.qc_decisions),
    )


def run_orchestrated_refresh(
    *,
    plan: OrchestrationPlan,
    policy: RefreshPolicy,
    report_family: str,
    period_start: datetime,
    period_end: datetime,
    observation_store: ObservationStore,
    snapshot_store: SnapshotStore,
    now: datetime | None = None,
) -> RefreshResult:
    """Execute registry-driven adapters through QC to a DRAFT snapshot."""
    observations, _skipped_sources = ingest_plan(plan)
    return run_refresh(
        policy=policy,
        project_id=plan.project_id,
        report_family=report_family,
        period_start=period_start,
        period_end=period_end,
        observations=observations,
        rules=plan.rules,
        observation_store=observation_store,
        snapshot_store=snapshot_store,
        now=now,
        approved_sources=frozenset(
            source for rule in plan.rules for source in rule.allowed_sources
        ),
    )


def run_due_engagements(
    *,
    policies: Iterable[RefreshPolicy],
    last_refresh: dict[str, datetime],
    refreshers: dict[str, Callable[[], RefreshResult]],
    now: datetime | None = None,
) -> list[RefreshResult]:
    current = now or datetime.now(timezone.utc)
    results: list[RefreshResult] = []
    for policy in policies:
        previous = last_refresh.get(policy.engagement_id)
        due = policy.enabled and (previous is None or current >= next_refresh(previous, policy))
        if due and policy.engagement_id in refreshers:
            results.append(refreshers[policy.engagement_id]())
    return results
