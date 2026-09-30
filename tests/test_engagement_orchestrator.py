from src.reporting.engagement_orchestrator import build_plan, load_engagements
from src.reporting.reportable_data import EvidenceClass, Location


def test_engagement_registry_drives_plan():
    engagements = load_engagements()
    engagement = engagements["ENG-S5-LAGOS"]
    plan = build_plan(
        engagement,
        project_id="S5-GLOBAL-LAGOS",
        site_id="lagos-reference-grid",
        location=Location(6.5, 3.4),
    )

    assert plan.engagement.reporting_frequency == "DAILY"
    assert "open-meteo-forecast" in [adapter.source_id for adapter in plan.adapters]
    assert "open-meteo-archive" in plan.skipped_sources
    assert plan.rules[0].minimum_evidence_class in {
        EvidenceClass.CONTEXTUAL,
        EvidenceClass.MODELED,
    }


def test_missing_project_coordinates_are_not_invented():
    engagements = load_engagements()
    engagement = engagements["ENG-S6C-LAGOS"]
    try:
        build_plan(
            engagement,
            project_id="S6C",
            site_id="lagos-s6c",
            location=None,
        )
    except (TypeError, AttributeError):
        pass
    else:
        raise AssertionError("orchestration must receive authorized coordinates explicitly")
