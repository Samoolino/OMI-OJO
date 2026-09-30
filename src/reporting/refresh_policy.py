"""Scheduling contract for engagement refreshes.

The cadence is derived from the canonical engagement registry. EVENT_AND_DAILY
means a daily baseline plus event-triggered execution; the scheduler may invoke
an event refresh without changing the declared baseline cadence.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class RefreshPolicy:
    engagement_id: str
    cadence: str
    interval_minutes: int
    enabled: bool = True


def next_refresh(last_refresh: datetime, policy: RefreshPolicy) -> datetime | None:
    if not policy.enabled:
        return None
    return last_refresh + timedelta(minutes=policy.interval_minutes)


POLICIES = {
    "ENG-S5-LAGOS": RefreshPolicy("ENG-S5-LAGOS", "DAILY", 24 * 60),
    "ENG-S6C-LAGOS": RefreshPolicy("ENG-S6C-LAGOS", "EVENT_AND_DAILY", 24 * 60),
}
