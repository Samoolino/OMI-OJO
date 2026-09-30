from datetime import datetime, timezone

from src.reporting.reportable_data import (
    EvidenceClass,
    Location,
    Observation,
    ReportabilityState,
    ReportingRule,
    evaluate_reportability,
)


NOW = datetime(2026, 9, 30, 12, 0, tzinfo=timezone.utc)


def rule(**overrides):
    values = dict(
        project_id="S6C",
        site_id="site-1",
        indicator_id="rainfall",
        allowed_sources=frozenset({"open-meteo-forecast"}),
        minimum_evidence_class=EvidenceClass.CONTEXTUAL,
        location=Location(6.5244, 3.3792),
        spatial_tolerance_degrees=0.05,
        max_age_seconds=86400,
    )
    values.update(overrides)
    return ReportingRule(**values)


def observation(**overrides):
    values = dict(
        observation_id="obs-1",
        project_id="S6C",
        site_id="site-1",
        indicator_id="rainfall",
        observed_at=NOW,
        location=Location(6.525, 3.379),
        value=12.4,
        unit="mm",
        source_id="open-meteo-forecast",
        evidence_class=EvidenceClass.CONTEXTUAL,
        qc_passed=True,
    )
    values.update(overrides)
    return Observation(**values)


def test_location_matched_contextual_observation_is_reportable_when_rule_allows_it():
    decision = evaluate_reportability(observation(), rule(), now=NOW)
    assert decision.state is ReportabilityState.REPORTABLE


def test_remote_source_cannot_satisfy_measured_requirement():
    decision = evaluate_reportability(
        observation(),
        rule(minimum_evidence_class=EvidenceClass.MEASURED),
        now=NOW,
    )
    assert decision.state is ReportabilityState.CONTEXTUAL_ONLY


def test_wrong_location_is_not_reportable():
    decision = evaluate_reportability(
        observation(location=Location(6.8, 3.8)),
        rule(),
        now=NOW,
    )
    assert decision.state is ReportabilityState.OUT_OF_BOUNDARY


def test_unapproved_source_is_not_reportable():
    decision = evaluate_reportability(
        observation(source_id="unknown-provider"),
        rule(),
        now=NOW,
    )
    assert decision.state is ReportabilityState.SOURCE_UNAPPROVED


def test_failed_qc_is_quarantined():
    decision = evaluate_reportability(observation(qc_passed=False), rule(), now=NOW)
    assert decision.state is ReportabilityState.QUARANTINED
