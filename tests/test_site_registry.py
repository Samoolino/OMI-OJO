from pathlib import Path

import pytest

from src.reporting.site_registry import SiteAuthorizationError, SiteRegistry


REGISTRY = Path("config/site-registry.json")


def test_pending_site_cannot_authorize_coordinates():
    registry = SiteRegistry.load(REGISTRY)
    with pytest.raises(SiteAuthorizationError, match="SITE_LOCATION_NOT_AUTHORIZED"):
        registry.resolve(project_id="S6C", site_id="lagos-s6c")


def test_unknown_site_is_rejected():
    registry = SiteRegistry.load(REGISTRY)
    with pytest.raises(SiteAuthorizationError, match="SITE_NOT_REGISTERED"):
        registry.resolve(project_id="S6C", site_id="unknown-site")


def test_project_site_mismatch_is_rejected():
    registry = SiteRegistry.load(REGISTRY)
    with pytest.raises(SiteAuthorizationError, match="SITE_PROJECT_MISMATCH"):
        registry.resolve(project_id="S5-GLOBAL-LAGOS", site_id="lagos-s6c")
