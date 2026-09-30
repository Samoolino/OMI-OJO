from __future__ import annotations

from src.reporting.agentic_collection import build_collection_actions


def test_agentic_collection_never_authorizes_physical_sources() -> None:
    actions = build_collection_actions()
    field_actions = [a for a in actions if a.source_id != "open-meteo-forecast"]
    assert field_actions
    assert all(a.action == "HOLD" for a in field_actions)


def test_only_registered_context_adapter_is_executable() -> None:
    actions = build_collection_actions()
    executable = [a for a in actions if a.action == "EXECUTE_CONTEXT_ADAPTER"]
    assert executable
    assert all(a.source_id == "open-meteo-forecast" for a in executable)
