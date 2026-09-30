"""Canonical Global Lagos source-to-node planning.

The planner expands the registered 40-node venue set into explicit
node × indicator × source plans. It is descriptive and gate-aware: it never
promotes candidate coordinates to authorization and never promotes evidence.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CONFIG = Path("config/global-lagos-source-bindings.json")
VENUES = Path("config/global-lagos-venues.json")

EXECUTABLE_ADAPTERS = {"open-meteo-forecast"}


def _load() -> tuple[dict[str, Any], dict[str, Any]]:
    return (
        json.loads(CONFIG.read_text(encoding="utf-8")),
        json.loads(VENUES.read_text(encoding="utf-8")),
    )


def build_global_lagos_plan() -> list[dict[str, Any]]:
    bindings, venues = _load()
    capabilities = bindings["source_capabilities"]
    class_bindings = bindings["class_bindings"]
    plan: list[dict[str, Any]] = []

    indicators = sorted(
        {indicator for mapping in class_bindings.values() for indicator in mapping}
    )
    refresh = {
        "rainfall": "DAILY", "temperature": "DAILY", "relative_humidity": "DAILY",
        "wind_speed": "DAILY", "solar_radiation": "DAILY", "air_quality": "HOURLY",
        "no2": "DAILY", "pm25": "HOURLY", "water_quality": "EVENT",
        "collection_volume": "EVENT", "ghg_activity_data": "PERIODIC",
        "esg_controls": "PERIODIC",
    }

    report_families = {
        "LCDA_REFERENCE": ["project_status", "environmental_data", "climate", "water", "esg", "ghg", "dmrv_evidence"],
        "STATE_INSTITUTION": ["project_status", "climate", "esg", "dmrv_evidence", "regulatory_audit"],
        "ENVIRONMENTAL_REFERENCE": ["project_status", "climate", "esg", "dmrv_evidence", "regulatory_audit"],
    }

    for node in venues["nodes"]:
        node_class = node["class"]
        for indicator in indicators:
            for source_id in class_bindings.get(node_class, {}).get(indicator, []):
                capability = capabilities[source_id]
                requires_gis = bool(capability["requires_authorized_gis"])
                if requires_gis:
                    state = "BLOCKED_PENDING_GIS"
                elif source_id in EXECUTABLE_ADAPTERS:
                    state = "CONTEXT_PLAN"
                else:
                    state = "UNSUPPORTED_ADAPTER"

                plan.append({
                    "node_id": node["id"],
                    "node_class": node_class,
                    "indicator_id": indicator,
                    "source_id": source_id,
                    "evidence_class": capability["evidence_class"],
                    "source_capability": capability["state"],
                    "refresh": refresh[indicator],
                    "requires_authorized_gis": requires_gis,
                    "authorization_required": requires_gis or source_id == "esg-control-register",
                    "qc_rule": (
                        "location_match + time_match + qc + custody/authorization"
                        if requires_gis
                        else "provider provenance + timestamp + schema/QC"
                    ),
                    "report_families": report_families[node_class],
                    "state": state,
                })

    return plan


def summarize_global_lagos_plan() -> dict[str, Any]:
    plan = build_global_lagos_plan()
    node_ids = {item["node_id"] for item in plan}
    return {
        "schema_version": "UB-02.LAGOS.ORCHESTRATION.1",
        "node_count": 40,
        "nodes_with_bindings": len(node_ids),
        "binding_count": len(plan),
        "states": {
            "context": sum(x["state"] == "CONTEXT_PLAN" for x in plan),
            "ready_for_authorized_collection": 0,
            "blocked_pending_gis": sum(x["state"] == "BLOCKED_PENDING_GIS" for x in plan),
            "unsupported_adapter": sum(x["state"] == "UNSUPPORTED_ADAPTER" for x in plan),
        },
        "rules": [
            "Pending or candidate GIS status blocks physical/field collection.",
            "Candidate public coordinates never authorize field collection.",
            "Modeled, satellite, measured and verified evidence classes remain distinct.",
            "The orchestration plan does not release reporting snapshots.",
        ],
        "plan": plan,
    }
