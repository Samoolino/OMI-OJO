"""Collection-asset and first-flush control state machine."""
from enum import StrEnum


class CollectionStatus(StrEnum):
    AVAILABLE = "AVAILABLE"
    SANITIZED = "SANITIZED"
    CALIBRATED = "CALIBRATED"
    DEPLOYED = "DEPLOYED"
    ARMED = "ARMED"
    COLLECTING = "COLLECTING"
    FIRST_FLUSH = "FIRST_FLUSH"
    PREMIUM_COLLECTION = "PREMIUM_COLLECTION"
    HARVEST_COMPLETE = "HARVEST_COMPLETE"
    CLEANING = "CLEANING"


def transition(current: CollectionStatus, target: CollectionStatus) -> CollectionStatus:
    allowed = {
        CollectionStatus.AVAILABLE: {CollectionStatus.SANITIZED},
        CollectionStatus.SANITIZED: {CollectionStatus.CALIBRATED},
        CollectionStatus.CALIBRATED: {CollectionStatus.DEPLOYED},
        CollectionStatus.DEPLOYED: {CollectionStatus.ARMED},
        CollectionStatus.ARMED: {CollectionStatus.COLLECTING},
        CollectionStatus.COLLECTING: {CollectionStatus.FIRST_FLUSH},
        CollectionStatus.FIRST_FLUSH: {CollectionStatus.PREMIUM_COLLECTION, CollectionStatus.HARVEST_COMPLETE},
        CollectionStatus.PREMIUM_COLLECTION: {CollectionStatus.HARVEST_COMPLETE},
        CollectionStatus.HARVEST_COMPLETE: {CollectionStatus.CLEANING},
        CollectionStatus.CLEANING: {CollectionStatus.AVAILABLE},
    }
    if target not in allowed[current]:
        raise ValueError(f"invalid collection transition: {current} -> {target}")
    return target


def premium_collection_allowed(first_flush_complete: bool, quality_gate_passed: bool) -> bool:
    return bool(first_flush_complete and quality_gate_passed)
