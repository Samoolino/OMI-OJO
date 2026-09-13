"""Integration helpers connecting measured rainfall telemetry to event state.

This is an orchestration boundary: it does not invent rainfall. A configured
minimum depth threshold determines whether a measured observation can advance
an event from detection to active/complete states.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from .events import RainEventStatus, transition
from .ingestion import Observation


@dataclass(frozen=True)
class RainfallEvent:
    event_id: str
    status: RainEventStatus
    source_id: str
    started_at: str
    cumulative_mm: float
    observation_ids: tuple[str, ...]


def detect_event(
    observation: Observation,
    *,
    minimum_event_depth_mm: float = 0.1,
) -> RainfallEvent:
    """Create a detected event from one MEASURED precipitation observation."""
    if observation.variable != "precipitation":
        raise ValueError("event detection requires precipitation observations")
    if observation.data_status != "MEASURED":
        raise ValueError("event detection requires MEASURED telemetry")
    if observation.value < minimum_event_depth_mm:
        raise ValueError("observation does not meet event depth threshold")

    seed = json.dumps(
        {
            "source_id": observation.source_id,
            "observed_at": observation.observed_at,
            "observation_id": observation.observation_id,
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    event_id = "rain_evt_" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:24]
    status = transition(RainEventStatus.NO_EVENT, RainEventStatus.RAIN_EVENT_DETECTED)
    return RainfallEvent(
        event_id=event_id,
        status=status,
        source_id=observation.source_id,
        started_at=observation.observed_at,
        cumulative_mm=observation.value,
        observation_ids=(observation.observation_id,),
    )


def activate_event(event: RainfallEvent) -> RainfallEvent:
    status = transition(event.status, RainEventStatus.RAIN_EVENT_ACTIVE)
    return RainfallEvent(**{**event.__dict__, "status": status})


def complete_event(event: RainfallEvent) -> RainfallEvent:
    status = transition(event.status, RainEventStatus.RAIN_EVENT_COMPLETE)
    return RainfallEvent(**{**event.__dict__, "status": status})


def append_measurement(event: RainfallEvent, observation: Observation) -> RainfallEvent:
    if observation.data_status != "MEASURED":
        raise ValueError("event measurements must be MEASURED")
    if observation.source_id != event.source_id:
        raise ValueError("event source does not match observation source")
    return RainfallEvent(
        **{
            **event.__dict__,
            "cumulative_mm": event.cumulative_mm + observation.value,
            "observation_ids": event.observation_ids + (observation.observation_id,),
        }
    )
