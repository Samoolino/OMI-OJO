"""Persistent history for canonical reporting snapshots."""
from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict
from pathlib import Path
from typing import Iterable

from .reporting_snapshot import ReportingSnapshot


class SnapshotStore:
    def __init__(self, path: str = "data/reporting/observations.db") -> None:
        self.path = path
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(path) as db:
            db.execute("""
              CREATE TABLE IF NOT EXISTS reporting_snapshots (
                snapshot_id TEXT PRIMARY KEY,
                project_id TEXT NOT NULL,
                report_family TEXT NOT NULL,
                period_start TEXT NOT NULL,
                period_end TEXT NOT NULL,
                created_at TEXT NOT NULL,
                release_state TEXT NOT NULL,
                deterministic_hash TEXT NOT NULL,
                payload_json TEXT NOT NULL
              )
            """)
            db.execute("""
              CREATE INDEX IF NOT EXISTS idx_snapshots_project_period
              ON reporting_snapshots(project_id, period_start, period_end)
            """)
            db.commit()

    def save(self, snapshot: ReportingSnapshot) -> bool:
        payload = json.dumps(asdict(snapshot), sort_keys=True, separators=(",", ":"))
        with sqlite3.connect(self.path) as db:
            cur = db.execute(
                """INSERT OR IGNORE INTO reporting_snapshots
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    snapshot.snapshot_id, snapshot.project_id, snapshot.report_family,
                    snapshot.reporting_period_start, snapshot.reporting_period_end,
                    snapshot.created_at, snapshot.release_state,
                    snapshot.deterministic_hash, payload,
                ),
            )
            db.commit()
            return cur.rowcount == 1

    def latest(self, project_id: str, report_family: str) -> dict | None:
        with sqlite3.connect(self.path) as db:
            row = db.execute(
                """SELECT payload_json FROM reporting_snapshots
                   WHERE project_id = ? AND report_family = ?
                   ORDER BY period_end DESC, created_at DESC LIMIT 1""",
                (project_id, report_family),
            ).fetchone()
        return json.loads(row[0]) if row else None

    def history(self, project_id: str, report_family: str, limit: int = 20) -> list[dict]:
        with sqlite3.connect(self.path) as db:
            rows = db.execute(
                """SELECT payload_json FROM reporting_snapshots
                   WHERE project_id = ? AND report_family = ?
                   ORDER BY period_end DESC, created_at DESC LIMIT ?""",
                (project_id, report_family, limit),
            ).fetchall()
        return [json.loads(row[0]) for row in rows]
