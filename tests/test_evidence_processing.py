from __future__ import annotations

from datetime import datetime, timezone, timedelta

from src.reporting.evidence_processing import (
    EvidenceQCState,
    build_evidence_package,
    process_evidence,
    evaluate_qc_then_reportability,
)
from src.reporting.reportable_data import EvidenceClass, Location, Observation, ReportingRule, ReportabilityState


NOW = datetime(2026, 9, 30, 12, 0, tzinfo=timezone.utc)


def obs(**overrides):
    base = dict(
        observation_id="ro-test-1",
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
    base.update(overrides)
    return Observation(**base)


def test_valid_remote_context_passes_qc_without_promotion():
    passed, decisions = process_evidence(
        [obs()],
        approved_sources=frozenset({"open-meteo-forecast"}),
        now=NOW,
    )
    assert len(passed) == 1
    assert decisions[0].state == EvidenceQCState.QC_PASSED
    assert passed[0].evidence_class is EvidenceClass.MODELED


def test_missing_provenance_is_quarantined():
    broken = obs(metadata={"provider": "Open-Meteo"})
    _, decisions = process_evidence(
        [broken],
        approved_sources=frozenset({"open-meteo-forecast"}),
        now=NOW,
    )
    assert decisions[0].state == EvidenceQCState.QUARANTINED


def test_stale_observation_is_not_reportable():
    stale = obs(observed_at=NOW - timedelta(days=3))
    _, decisions = process_evidence(
        [stale],
        approved_sources=frozenset({"open-meteo-forecast"}),
        now=NOW,
    )
    assert decisions[0].state == EvidenceQCState.STALE


def test_location_mismatch_is_out_of_boundary():
    wrong = obs(location=Location(7.5, 4.0))
    _, decisions = process_evidence(
        [wrong],
        approved_sources=frozenset({"open-meteo-forecast"}),
        now=NOW,
        location=(6.62, 3.36),
    )
    assert decisions[0].state == EvidenceQCState.OUT_OF_BOUNDARY


def test_unapproved_source_is_explicit():
    wrong = obs(source_id="unapproved-provider")
    _, decisions = process_evidence(
        [wrong],
        approved_sources=frozenset({"open-meteo-forecast"}),
        now=NOW,
    )
    assert decisions[0].state == EvidenceQCState.SOURCE_UNAPPROVED


def test_evidence_package_hash_is_deterministic():
    observations = [obs()]
    _, decisions = process_evidence(
        observations,
        approved_sources=frozenset({"open-meteo-forecast"}),
        now=NOW,
    )
    a = build_evidence_package(observations, decisions, created_at=NOW)
    b = build_evidence_package(observations, decisions, created_at=NOW)
    assert a.package_id == b.package_id
    assert a.package_hash == b.package_hash


def test_reportability_occurs_only_after_qc():
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
    package, decisions, reportability = evaluate_qc_then_reportability(
        [obs()],
        [rule],
        approved_sources=frozenset({"open-meteo-forecast"}),
        now=NOW,
    )
    assert package.qc_passed_ids == ("ro-test-1",)
    assert decisions[0].state == EvidenceQCState.QC_PASSED
    assert reportability[0].state == ReportabilityState.REPORTABLE
    assert reportability[0].observation_id in package.qc_passed_ids
