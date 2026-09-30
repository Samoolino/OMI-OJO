"""Governed refresh orchestration.

The worker is intentionally source-adapter agnostic. A deployment scheduler calls
run_refresh with observations retrieved by an approved adapter. This keeps
provider I/O, project rules, persistence, and publication boundaries separate.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable, Iterable

from .observation_store import ObservationStore
from .refresh_policy import RefreshPolicy, next_refresh
from .reportable_data import Observation, ReportingRule, evaluate_batch
from .reporting_snapshot import ReportingSnapshot, build_snapshot
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
) -> RefreshResult:
    """Persist observations, evaluate reportability, and persist one snapshot."""
    current = now or datetime.now(timezone.utc)
    items = list(observations)
    observation_store.upsert(items)

    decisions = evaluate_batch(items, rules, now=current)
    snapshot = build_snapshot(
        project_id=project_id,
        report_family=report_family,
        period_start=period_start,
        period_end=period_end,
        observations=items,
        decisions=decisions,
        release_state="DRAFT",
    )
    snapshot_store.save(snapshot)

    scheduled = next_refresh(current, policy)
    return RefreshResult(
        engagement_id=policy.engagement_id,
        project_id=project_id,
        report_family=report_family,
        ingested=len(items),
        decisions=len(decisions),
        snapshot_id=snapshot.snapshot_id,
        snapshot_hash=snapshot.deterministic_hash,
        next_refresh_at=scheduled.isoformat() if scheduled else None,
    )


def run_due_engagements(
    *,
    policies: Iterable[RefreshPolicy],
    last_refresh: dict[str, datetime],
    refreshers: dict[str, Callable[[], RefreshResult]],
    now: datetime | None = None,
) -> list[RefreshResult]:
    """Run only policies whose declared cadence is due.

    A scheduler owns the durable last-refresh ledger; this function only evaluates
    due-ness and executes the supplied governed refresh callbacks.
    """
    current = now or datetime.now(timezone.utc)
    results: list[RefreshResult] = []
    for policy in policies:
        previous = last_refresh.get(policy.engagement_id)
        due = policy.enabled and (previous is None or current >= next_refresh(previous, policy))
        if due and policy.engagement_id in refreshers:
            results.append(refreshers[policy.engagement_id]())
    return results
