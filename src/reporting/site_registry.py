"""Canonical project/site coordinate authorization boundary.

The registry deliberately refuses to manufacture coordinates. A site becomes
usable for physical-source orchestration only after an authorized GIS record
sets status=AUTHORIZED and records its coordinate provenance/version.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .reportable_data import Location


class SiteAuthorizationError(ValueError):
    """Raised when a project/site cannot authorize a physical location."""


@dataclass(frozen=True)
class SiteRecord:
    site_id: str
    project_ids: tuple[str, ...]
    geography: dict
    status: str
    latitude: float | None
    longitude: float | None
    coordinate_source: str | None
    coordinate_version: str | None


class SiteRegistry:
    def __init__(self, sites: dict[str, SiteRecord]):
        self.sites = sites

    @classmethod
    def load(cls, path: str | Path = "config/site-registry.json") -> "SiteRegistry":
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        records: dict[str, SiteRecord] = {}
        for raw in payload.get("sites", []):
            records[raw["site_id"]] = SiteRecord(
                site_id=raw["site_id"],
                project_ids=tuple(raw.get("project_ids", [])),
                geography=dict(raw.get("geography", {})),
                status=raw["status"],
                latitude=raw.get("latitude"),
                longitude=raw.get("longitude"),
                coordinate_source=raw.get("coordinate_source"),
                coordinate_version=raw.get("coordinate_version"),
            )
        return cls(records)

    def resolve(self, *, project_id: str, site_id: str) -> Location:
        record = self.sites.get(site_id)
        if record is None:
            raise SiteAuthorizationError("SITE_NOT_REGISTERED")
        if project_id not in record.project_ids:
            raise SiteAuthorizationError("SITE_PROJECT_MISMATCH")
        if record.status != "AUTHORIZED":
            raise SiteAuthorizationError("SITE_LOCATION_NOT_AUTHORIZED")
        if record.latitude is None or record.longitude is None:
            raise SiteAuthorizationError("SITE_COORDINATES_MISSING")
        if not (-90 <= record.latitude <= 90 and -180 <= record.longitude <= 180):
            raise SiteAuthorizationError("SITE_COORDINATES_INVALID")
        if not record.coordinate_source or not record.coordinate_version:
            raise SiteAuthorizationError("SITE_COORDINATE_PROVENANCE_MISSING")
        return Location(latitude=record.latitude, longitude=record.longitude)

    def describe(self, *, project_id: str, site_id: str) -> dict:
        record = self.sites.get(site_id)
        if record is None:
            return {"state": "SITE_NOT_REGISTERED", "site_id": site_id}
        if project_id not in record.project_ids:
            return {"state": "SITE_PROJECT_MISMATCH", "site_id": site_id, "project_id": project_id}
        return {
            "state": record.status,
            "site_id": record.site_id,
            "project_id": project_id,
            "latitude": record.latitude,
            "longitude": record.longitude,
            "coordinate_source": record.coordinate_source,
            "coordinate_version": record.coordinate_version,
        }
