from __future__ import annotations

from datetime import datetime, timezone, timedelta

from src.reporting.refresh_worker import run_refresh
from src.reporting.observation_store import ObservationStore
from src.reporting.snapshot_store import SnapshotStore
from src.reporting.refresh_policy import RefreshPolicy
from src.reporting.reportable_data import EvidenceClass, Location, Observation, ReportingRule, ReportabilityState


NOW = datetime(2026, 9, 30, 12, 0, tzinfo=timezone.utc)


def test_refresh_persists_only_qc_passed_data_and_creates_draft_snapshot(tmp_path):
    valid = Observation(
        observation_id="ro-refresh-1",
        project_id="S5-GLOBAL-LAGOS",
        site_id="lagos-reference-grid",
        indicator_id="rainfall",
        observed_at=NOW - timedelta(hours=1),
        location=Location(6.62, 3.36),
        value=4.2,
        unit="mm",
        source_id="open-meteo-forecast",
        evidence_class=EvidenceClass.MODELED,
        qc_passed=True,
        metadata={
            "provider": "Open-Meteo",
            "source_snapshot_id": "snap-1",
            "methodology_status": "REMOTE_CONTEXT_ONLY",
        },
    )
    stale = Observation(
        **{**valid.__dict__, "observation_id": "ro-refresh-stale", "observed_at": NOW - timedelta(days=3)}
    )
    rule = ReportingRule(
        project_id="S5-GLOBAL-LAGOS",
        site_id="lagos-reference-grid",
        indicator_id="rainfall",
        allowed_sources=frozenset({"open-meteo-forecast"}),
        minimum_evidence_class=EvidenceClass.MODELED,
        location=Location(6.62, 3.36),
        spatial_tolerance_degrees=0.05,
        max_age_seconds=172800,
    )
    policy = RefreshPolicy(engagement_id="ENG-S5-LAGOS", cadence_minutes=1440, enabled=True)
    obs_store = ObservationStore(tmp_path / "reporting.db")
    snap_store = SnapshotStore(str(tmp_path / "reporting.db"))

    result = run_refresh(
        policy=policy,
        project_id="S5-GLOBAL-LAGOS",
        report_family="CLIMATE",
        period_start=NOW - timedelta(days=1),
        period_end=NOW,
        observations=[valid, stale],
        rules=[rule],
        observation_store=obs_store,
        snapshot_store=snap_store,
        now=NOW,
    )

    assert result.evidence_package_id
    assert result.qc_decisions == 2
    assert result.decisions == 1
    assert result.snapshot_id.startswith("RS-")
    latest = snap_store.latest("S5-GLOBAL-LAGOS", "CLIMATE")
    assert latest["release_state"] == "DRAFT"
    assert latest["reportable_observation_ids"] == ["ro-refresh-1"]
    assert "ro-refresh-stale" not in latest["reportable_observation_ids"]
    assert len(obs_store.list_project("S5-GLOBAL-LAGOS")) == 1
