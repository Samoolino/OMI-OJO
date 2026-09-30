from pathlib import Path

from src.reporting.engagement_registry import EngagementRegistry


ROOT = Path(__file__).resolve().parents[1]


def test_engagements_bind_to_explicit_work_packages():
    registry = EngagementRegistry(
        engagement_path=ROOT / "config/reporting-engagement-registry.json",
        binding_path=ROOT / "config/engagement-work-package-bindings.json",
    )
    binding = registry.validate("ENG-S6C-LAGOS", "S6C")
    assert "WP-02" in binding.work_package_ids
    assert binding.anchor_required is True


def test_cross_project_binding_is_rejected():
    registry = EngagementRegistry(
        engagement_path=ROOT / "config/reporting-engagement-registry.json",
        binding_path=ROOT / "config/engagement-work-package-bindings.json",
    )
    try:
        registry.validate("ENG-S6C-LAGOS", "S5-GLOBAL-LAGOS")
    except ValueError:
        return
    raise AssertionError("expected project scope rejection")
