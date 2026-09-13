"""Rainfall-event state machine."""
from enum import StrEnum


class RainEventStatus(StrEnum):
    NO_EVENT = "NO_EVENT"
    FORECASTED = "FORECASTED"
    RAIN_EVENT_DETECTED = "RAIN_EVENT_DETECTED"
    RAIN_EVENT_ACTIVE = "RAIN_EVENT_ACTIVE"
    RAIN_EVENT_COMPLETE = "RAIN_EVENT_COMPLETE"
    OBSERVED = "OBSERVED"
    RECONCILED = "RECONCILED"

_ALLOWED: dict[RainEventStatus, set[RainEventStatus]] = {
    RainEventStatus.NO_EVENT: {RainEventStatus.FORECASTED, RainEventStatus.RAIN_EVENT_DETECTED},
    RainEventStatus.FORECASTED: {RainEventStatus.RAIN_EVENT_DETECTED, RainEventStatus.NO_EVENT},
    RainEventStatus.RAIN_EVENT_DETECTED: {RainEventStatus.RAIN_EVENT_ACTIVE},
    RainEventStatus.RAIN_EVENT_ACTIVE: {RainEventStatus.RAIN_EVENT_COMPLETE},
    RainEventStatus.RAIN_EVENT_COMPLETE: {RainEventStatus.OBSERVED},
    RainEventStatus.OBSERVED: {RainEventStatus.RECONCILED},
    RainEventStatus.RECONCILED: {RainEventStatus.FORECASTED, RainEventStatus.NO_EVENT},
}


def transition(current: RainEventStatus, target: RainEventStatus) -> RainEventStatus:
    if target not in _ALLOWED[current]:
        raise ValueError(f"invalid rainfall transition: {current} -> {target}")
    return target
