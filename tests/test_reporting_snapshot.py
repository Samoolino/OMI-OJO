from datetime import datetime, timezone

from src.reporting.reportable_data import (
    EvidenceClass,
    Location,
    Observation,
    ReportingRule,
    evaluate_batch,
)
from src.reporting.reporting_snapshot import build_snapshot


def test_snapshot_contains_reportable_and_contextual_observations():
    now = datetime(2026, 9, 30, 12, 0, tzinfo=timezone.utc)
    observations = [
        Observation(
            observation_id="OBS-1",
            project_id="S6C",
            site_id="lagos-site-1",
            indicator_id="rainfall",
            observed_at=now,
            location=Location(6.50, 3.40),
            value=12.4,
            unit="mm",
            source_id="open-meteo",
            evidence_class=EvidenceClass.MODELED,
            qc_passed=True,
        ),
        Observation(
            observation_id="OBS-2",
            project_id="S6C",
            site_id="lagos-site-1",
            indicator_id="water-quality",
            observed_at=now,
            location=Location(6.50, 3.40),
            value="pass",
            unit="QMS",
            source_id="field-qms",
            evidence_class=EvidenceClass.VERIFIED_MEASUREMENT,
            qc_passed=True,
        ),
    ]
    rules = [
        ReportingRule("S6C", "lagos-site-1", "rainfall", frozenset({"open-meteo"}), EvidenceClass.MODELED, Location(6.50, 3.40), 0.1, 3600),
        ReportingRule("S6C", "lagos-site-1", "water-quality", frozenset({"field-qms"}), EvidenceClass.VERIFIED_MEASUREMENT, Location(6.50, 3.40), 0.1, 3600),
    ]
    decisions = evaluate_batch(observations, rules, now=now)
    snapshot = build_snapshot(
        project_id="S6C",
        report_family="environmental_data",
        period_start=now,
        period_end=now,
        observations=observations,
        decisions=decisions,
    )

    assert snapshot.reportable_observation_ids == ("OBS-1", "OBS-2")
    assert snapshot.contextual_observation_ids == ()
    assert snapshot.excluded_observation_ids == ()
    assert snapshot.deterministic_hash
    assert snapshot.snapshot_id.startswith("RS-")
