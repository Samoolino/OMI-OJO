"""Durable persistence contract.

Production storage is injected behind this interface. The reference SQLite stores
remain useful for local development, but the reporting domain does not depend on
a particular database vendor.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Sequence

from .reportable_data import Observation
from .reporting_snapshot import ReportingSnapshot


class ReportingPersistence(ABC):
    @abstractmethod
    def put_observations(self, observations: Sequence[Observation]) -> int:
        """Persist canonical observations idempotently."""

    @abstractmethod
    def put_snapshot(self, snapshot: ReportingSnapshot) -> bool:
        """Persist a versioned snapshot idempotently."""

    @abstractmethod
    def observations(self, project_id: str, start: datetime | None = None, end: datetime | None = None) -> list[dict]:
        """Return historical canonical observations."""

    @abstractmethod
    def snapshots(self, project_id: str, report_family: str, limit: int = 20) -> list[dict]:
        """Return historical reporting snapshots."""


class CompositeReportingPersistence(ReportingPersistence):
    """Reference composition for local/runtime deployments."""

    def __init__(self, observation_store, snapshot_store) -> None:
        self.observation_store = observation_store
        self.snapshot_store = snapshot_store

    def put_observations(self, observations: Sequence[Observation]) -> int:
        return self.observation_store.upsert(observations)

    def put_snapshot(self, snapshot: ReportingSnapshot) -> bool:
        return self.snapshot_store.save(snapshot)

    def observations(self, project_id: str, start=None, end=None) -> list[dict]:
        return self.observation_store.list_project(project_id, start, end)

    def snapshots(self, project_id: str, report_family: str, limit: int = 20) -> list[dict]:
        return self.snapshot_store.history(project_id, report_family, limit)
