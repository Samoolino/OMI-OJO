"""Gate-aware collection execution for the Global Lagos orchestration plan."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .evidence_processing import EvidencePackage, EvidenceQCDecision, build_evidence_package, process_evidence
from .global_lagos_orchestration import build_global_lagos_plan
from .reportable_data import Observation, EvidenceClass, Location
from .source_adapters import SourceRequest, adapter_for


@dataclass(frozen=True)
class CollectionAction:
    node_id: str
    indicator_id: str
    source_id: str
    state: str
    action: str
    reason: str


@dataclass(frozen=True)
class CollectionRun:
    actions: tuple[CollectionAction, ...]
    observations: tuple[Observation, ...]
    skipped: tuple[CollectionAction, ...]


@dataclass(frozen=True)
class EvidenceProcessingRun:
    package: EvidencePackage
    qc_decisions: tuple[EvidenceQCDecision, ...]
    reportable_observations: tuple[Observation, ...]


def build_collection_actions() -> tuple[CollectionAction, ...]:
    actions: list[CollectionAction] = []
    for item in build_global_lagos_plan():
        if item["state"] == "CONTEXT_PLAN":
            actions.append(CollectionAction(
                item["node_id"], item["indicator_id"], item["source_id"],
                item["state"], "EXECUTE_CONTEXT_ADAPTER",
                "registered executable remote/context source",
            ))
        elif item["state"] == "BLOCKED_PENDING_GIS":
            actions.append(CollectionAction(
                item["node_id"], item["indicator_id"], item["source_id"],
                item["state"], "HOLD",
                "physical/field source requires authorized GIS",
            ))
        else:
            actions.append(CollectionAction(
                item["node_id"], item["indicator_id"], item["source_id"],
                item["state"], "HOLD",
                "provider adapter is not executable",
            ))
    return tuple(actions)


def execute_context_collection(
    *,
    node_id: str,
    project_id: str,
    site_id: str,
    location: Location,
    indicator_ids: Sequence[str],
    source_id: str = "open-meteo-forecast",
) -> CollectionRun:
    if source_id != "open-meteo-forecast":
        raise ValueError("only the registered executable context adapter may execute")
    adapter = adapter_for(source_id)
    observations = adapter.ingest(SourceRequest(
        project_id=project_id,
        site_id=site_id,
        indicator_ids=tuple(indicator_ids),
        location=location,
        source_id=source_id,
    ))
    # Adapter output remains MODELED; this function never promotes evidence.
    if any(obs.evidence_class is not EvidenceClass.MODELED for obs in observations):
        raise ValueError("context collection attempted an evidence-class promotion")
    actions = build_collection_actions()
    skipped = tuple(a for a in actions if a.node_id == node_id and a.action == "HOLD")
    executed = tuple(a for a in actions if a.node_id == node_id and a.source_id == source_id)
    return CollectionRun(executed, tuple(observations), skipped)


def process_collection_evidence(
    collection: CollectionRun,
    *,
    approved_sources: frozenset[str],
    now=None,
    location: tuple[float, float] | None = None,
    max_age_seconds: int = 172800,
) -> EvidenceProcessingRun:
    """Run QC and package creation after collection, before reportability."""
    passed, decisions = process_evidence(
        collection.observations,
        approved_sources=approved_sources,
        now=now,
        location=location,
        max_age_seconds=max_age_seconds,
    )
    package = build_evidence_package(collection.observations, decisions)
    return EvidenceProcessingRun(
        package=package,
        qc_decisions=decisions,
        reportable_observations=passed,
    )
