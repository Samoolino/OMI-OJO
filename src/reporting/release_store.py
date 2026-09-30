from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict
from pathlib import Path

from .release_governance import ReleaseDecision


class ReleaseStore:
    """Persistent audit store for governed reporting release decisions."""

    def __init__(self, path: str = "data/reporting/releases.db") -> None:
        self.path = path
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(path) as db:
            db.execute(
                """CREATE TABLE IF NOT EXISTS release_decisions (
                    decision_id TEXT PRIMARY KEY,
                    snapshot_id TEXT NOT NULL,
                    evidence_package_id TEXT NOT NULL,
                    state TEXT NOT NULL,
                    decision_hash TEXT NOT NULL,
                    decided_at TEXT NOT NULL,
                    payload_json TEXT NOT NULL
                )"""
            )
            db.execute(
                "CREATE INDEX IF NOT EXISTS idx_release_snapshot ON release_decisions(snapshot_id, decided_at)"
            )
            db.commit()

    def save(self, decision: ReleaseDecision) -> bool:
        payload = json.dumps(asdict(decision), sort_keys=True, separators=(",", ":"))
        with sqlite3.connect(self.path) as db:
            cur = db.execute(
                """INSERT OR IGNORE INTO release_decisions
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    decision.decision_id,
                    decision.snapshot_id,
                    decision.evidence_package_id,
                    decision.state,
                    decision.deterministic_hash,
                    decision.decided_at,
                    payload,
                ),
            )
            db.commit()
            return cur.rowcount == 1

    def history(self, snapshot_id: str, limit: int = 50) -> list[dict]:
        with sqlite3.connect(self.path) as db:
            rows = db.execute(
                """SELECT payload_json FROM release_decisions
                   WHERE snapshot_id = ?
                   ORDER BY decided_at ASC LIMIT ?""",
                (snapshot_id, limit),
            ).fetchall()
        return [json.loads(row[0]) for row in rows]

    def latest(self, snapshot_id: str) -> dict | None:
        history = self.history(snapshot_id, limit=1_000_000)
        return history[-1] if history else None
