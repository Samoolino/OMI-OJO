"""Canonical reporting snapshot/read-model builder for OMI-OJO.

A snapshot is the governed boundary between source/dMRV processing and every
reporting surface. It contains only observations that have passed the project's
reportability contract while retaining rejected/contextual counts for auditability.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from typing import Iterable

from .reportable_data import Observation, ReportabilityDecision, ReportabilityState


@dataclass(frozen=True)
class ReportingSnapshot:
    schema_version: str
    snapshot_id: str
    created_at: str
    reporting_period_start: str
    reporting_period_end: str
    project_id: str
    site_ids: tuple[str, ...]
    report_family: str
    reportable_observation_ids: tuple[str, ...]
    contextual_observation_ids: tuple[str, ...]
    excluded_observation_ids: tuple[str, ...]
    indicator_ids: tuple[str, ...]
    source_ids: tuple[str, ...]
    release_state: str
    deterministic_hash: str


def build_snapshot(
    *,
    project_id: str,
    report_family: str,
    period_start: datetime,
    period_end: datetime,
    observations: Iterable[Observation],
    decisions: Iterable[ReportabilityDecision],
    release_state: str = "DRAFT",
) -> ReportingSnapshot:
    """Build a deterministic reporting read model from governed decisions."""
    observation_index = {o.observation_id: o for o in observations}
    decision_list = list(decisions)

    reportable = tuple(sorted(d.observation_id for d in decision_list if d.state == ReportabilityState.REPORTABLE))
    contextual = tuple(sorted(d.observation_id for d in decision_list if d.state == ReportabilityState.CONTEXTUAL_ONLY))
    excluded = tuple(sorted(d.observation_id for d in decision_list if d.state not in {ReportabilityState.REPORTABLE, ReportabilityState.CONTEXTUAL_ONLY}))

    included_ids = reportable + contextual
    included = [observation_index[i] for i in included_ids if i in observation_index]
    site_ids = tuple(sorted({o.site_id for o in included}))
    indicator_ids = tuple(sorted({o.indicator_id for o in included}))
    source_ids = tuple(sorted({o.source_id for o in included}))

    canonical = {
        "schema_version": "UB-02.REPORTING-SNAPSHOT.1",
        "project_id": project_id,
        "report_family": report_family,
        "period_start": period_start.astimezone(timezone.utc).isoformat(),
        "period_end": period_end.astimezone(timezone.utc).isoformat(),
        "reportable": reportable,
        "contextual": contextual,
        "excluded": excluded,
        "sites": site_ids,
        "indicators": indicator_ids,
        "sources": source_ids,
        "release_state": release_state,
    }
    payload = json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()
    snapshot_id = f"RS-{digest[:16]}"

    return ReportingSnapshot(
        schema_version=canonical["schema_version"],
        snapshot_id=snapshot_id,
        created_at=datetime.now(timezone.utc).isoformat(),
        reporting_period_start=canonical["period_start"],
        reporting_period_end=canonical["period_end"],
        project_id=project_id,
        site_ids=site_ids,
        report_family=report_family,
        reportable_observation_ids=reportable,
        contextual_observation_ids=contextual,
        excluded_observation_ids=excluded,
        indicator_ids=indicator_ids,
        source_ids=source_ids,
        release_state=release_state,
        deterministic_hash=digest,
    )


def snapshot_to_dict(snapshot: ReportingSnapshot) -> dict[str, object]:
    return asdict(snapshot)
