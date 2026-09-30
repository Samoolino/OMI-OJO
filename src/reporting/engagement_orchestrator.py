"""Engagement-driven source orchestration.

This module turns the reporting engagement registry into executable source
requests. It does not invent coordinates or enable unregistered providers.
Unsupported adapters are surfaced as skipped capabilities rather than silently
replaced.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .reportable_data import EvidenceClass, Location, ReportingRule
from .source_adapters import SourceAdapter, SourceRequest, adapter_for
from .site_registry import SiteRegistry


@dataclass(frozen=True)
class Engagement:
    engagement_id: str
    project_ids: tuple[str, ...]
    sites: tuple[str, ...]
    reporting_frequency: str
    indicators: tuple[str, ...]
    source_allowlist: tuple[str, ...]
    minimum_evidence_class: dict[str, EvidenceClass]
    report_templates: tuple[str, ...]


@dataclass(frozen=True)
class OrchestrationPlan:
    engagement: Engagement
    project_id: str
    site_id: str
    location: Location
    adapters: tuple[SourceAdapter, ...]
    skipped_sources: tuple[str, ...]
    rules: tuple[ReportingRule, ...]


def load_engagements(path: str | Path = "config/reporting-engagement-registry.json") -> dict[str, Engagement]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    result: dict[str, Engagement] = {}
    for raw in payload.get("engagements", []):
        minimum = {key: EvidenceClass(value) for key, value in raw.get("minimum_evidence_class", {}).items()}
        engagement = Engagement(
            engagement_id=raw["engagement_id"],
            project_ids=tuple(raw["project_ids"]),
            sites=tuple(raw["sites"]),
            reporting_frequency=raw["reporting_frequency"],
            indicators=tuple(raw["indicators"]),
            source_allowlist=tuple(raw["source_allowlist"]),
            minimum_evidence_class=minimum,
            report_templates=tuple(raw.get("report_templates", [])),
        )
        result[engagement.engagement_id] = engagement
    return result


def build_plan(
    engagement: Engagement,
    *,
    project_id: str,
    site_id: str,
    location: Location | None = None,
    site_registry: SiteRegistry | None = None,
    max_age_seconds: int = 172800,
) -> OrchestrationPlan:
    if location is None:
        registry = site_registry or SiteRegistry.load()
        location = registry.resolve(project_id=project_id, site_id=site_id)
    if project_id not in engagement.project_ids:
        raise ValueError("project is not part of engagement")
    if site_id not in engagement.sites:
        raise ValueError("site is not part of engagement")

    adapters: list[SourceAdapter] = []
    skipped: list[str] = []
    for source_id in engagement.source_allowlist:
        try:
            adapters.append(adapter_for(source_id))
        except ValueError:
            skipped.append(source_id)

    rules = tuple(
        ReportingRule(
            project_id=project_id,
            site_id=site_id,
            indicator_id=indicator,
            allowed_sources=frozenset(engagement.source_allowlist),
            minimum_evidence_class=engagement.minimum_evidence_class.get(indicator, EvidenceClass.CONTEXTUAL),
            location=location,
            spatial_tolerance_degrees=0.05,
            max_age_seconds=max_age_seconds,
            require_qc=True,
            require_reconciliation=False,
        )
        for indicator in engagement.indicators
    )
    return OrchestrationPlan(engagement, project_id, site_id, location, tuple(adapters), tuple(skipped), rules)


def ingest_plan(plan: OrchestrationPlan) -> tuple[list, tuple[str, ...]]:
    observations = []
    for source_adapter in plan.adapters:
        observations.extend(source_adapter.ingest(SourceRequest(
            project_id=plan.project_id,
            site_id=plan.site_id,
            indicator_ids=plan.engagement.indicators,
            location=plan.location,
            source_id=source_adapter.source_id,
        )))
    return observations, plan.skipped_sources
