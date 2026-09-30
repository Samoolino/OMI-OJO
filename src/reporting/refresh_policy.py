"""Scheduling contract for engagement refreshes.

Scheduling is declarative here; deployment workers can execute it without
embedding project-specific rules in the frontend.
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
    "ENG-S5-LAGOS": RefreshPolicy("ENG-S5-LAGOS", "hourly", 60),
    "ENG-S6C-LAGOS": RefreshPolicy("ENG-S6C-LAGOS", "hourly", 60),
}
