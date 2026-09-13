from datetime import datetime, timezone

from src.production.collection import CollectionStatus, premium_collection_allowed, transition as collection_transition
from src.production.events import RainEventStatus, transition as event_transition
from src.production.evidence import build_evidence_package
from src.production.planning import make_collection_plan
from src.production.provenance import sha256_hex
from src.production.volume import gross_volume_liters, usable_volume_liters


def test_volume_equation():
    assert gross_volume_liters(10, 10, 1, 1) == 100
    assert usable_volume_liters(100, 10, 5, 5) == 80


def test_collection_plan():
    plan = make_collection_plan("E1", 10, 10, 1, 1, 0, 0, 0, 50)
    assert plan.expected_usable_liters == 100
    assert plan.required_bags == 3


def test_first_flush_gate():
    assert premium_collection_allowed(False, True) is False
    assert premium_collection_allowed(True, True) is True


def test_event_state_machine():
    state = event_transition(RainEventStatus.NO_EVENT, RainEventStatus.FORECASTED)
    state = event_transition(state, RainEventStatus.RAIN_EVENT_DETECTED)
    assert state == RainEventStatus.RAIN_EVENT_DETECTED


def test_collection_state_machine():
    state = collection_transition(CollectionStatus.AVAILABLE, CollectionStatus.SANITIZED)
    assert state == CollectionStatus.SANITIZED


def test_deterministic_evidence():
    a = {"batch": "B1", "volume": 10}
    assert sha256_hex(a) == sha256_hex(a)
    package = build_evidence_package(a, "BE-0.1")
    assert len(package.evidence_root) == 64
