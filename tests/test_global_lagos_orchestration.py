from __future__ import annotations

import json
from pathlib import Path

from src.reporting.global_lagos_orchestration import (
    build_global_lagos_plan,
    summarize_global_lagos_plan,
)


def test_global_lagos_plan_covers_all_40_nodes() -> None:
    plan = build_global_lagos_plan()
    assert plan
    node_ids = {item["node_id"] for item in plan}
    registry = json.loads(Path("config/global-lagos-venues.json").read_text(encoding="utf-8"))
    assert len(registry["nodes"]) == 40
    assert node_ids == {node["id"] for node in registry["nodes"]}


def test_pending_gis_blocks_field_sources() -> None:
    plan = build_global_lagos_plan()
    blocked = [item for item in plan if item["state"] == "BLOCKED_PENDING_GIS"]
    assert blocked
    assert all(item["requires_authorized_gis"] for item in blocked)


def test_context_execution_is_limited_to_registered_adapters() -> None:
    plan = build_global_lagos_plan()
    context = [item for item in plan if item["state"] == "CONTEXT_PLAN"]
    unsupported = [item for item in plan if item["state"] == "UNSUPPORTED_ADAPTER"]
    assert context
    assert unsupported
    assert all(not item["requires_authorized_gis"] for item in context)
    assert all(item["source_id"] == "open-meteo-forecast" for item in context)


def test_summary_has_exact_node_coverage() -> None:
    summary = summarize_global_lagos_plan()
    assert summary["node_count"] == 40
    assert summary["nodes_with_bindings"] == 40
    assert summary["states"]["ready_for_authorized_collection"] == 0
