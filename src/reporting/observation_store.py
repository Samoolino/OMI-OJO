"""SQLite-backed canonical observation store for UB-02 reporting.

The store is deliberately provider-neutral: adapters write canonical observations,
while reportability and snapshot layers decide what may be published.
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Iterable

from .reportable_data import Observation


class ObservationStore:
    def __init__(self, path: str | Path = "data/reporting/observations.db") -> None:
        self.path = str(path)
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init(self) -> None:
        with self._connect() as db:
            db.execute("""
              CREATE TABLE IF NOT EXISTS observations (
                observation_id TEXT PRIMARY KEY,
                project_id TEXT NOT NULL,
                site_id TEXT NOT NULL,
                indicator_id TEXT NOT NULL,
                observed_at TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                value_json TEXT NOT NULL,
                unit TEXT NOT NULL,
                source_id TEXT NOT NULL,
                evidence_class TEXT NOT NULL,
                qc_passed INTEGER NOT NULL,
                content_hash TEXT NOT NULL,
                ingested_at TEXT NOT NULL
              )
            """)
            db.execute("CREATE INDEX IF NOT EXISTS idx_obs_project_time ON observations(project_id, observed_at)")
            db.execute("CREATE INDEX IF NOT EXISTS idx_obs_project_indicator ON observations(project_id, indicator_id)")
            db.commit()

    def upsert(self, observations: Iterable[Observation]) -> int:
        count = 0
        with self._connect() as db:
            for o in observations:
                raw = json.dumps({
                    "observation_id": o.observation_id,
                    "project_id": o.project_id,
                    "site_id": o.site_id,
                    "indicator_id": o.indicator_id,
                    "observed_at": o.observed_at.isoformat(),
                    "lat": o.location.latitude,
                    "lon": o.location.longitude,
                    "value": o.value,
                    "unit": o.unit,
                    "source_id": o.source_id,
                    "evidence_class": o.evidence_class.value,
                    "qc_passed": o.qc_passed,
                }, sort_keys=True, separators=(",", ":"))
                digest = hashlib.sha256(raw.encode()).hexdigest()
                db.execute("""
                  INSERT OR IGNORE INTO observations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    o.observation_id, o.project_id, o.site_id, o.indicator_id,
                    o.observed_at.isoformat(), o.location.latitude, o.location.longitude,
                    json.dumps(o.value), o.unit, o.source_id, o.evidence_class.value,
                    int(o.qc_passed), digest, datetime.utcnow().isoformat() + "Z",
                ))
                count += 1
            db.commit()
        return count

    def list_project(self, project_id: str, start: datetime | None = None, end: datetime | None = None) -> list[dict]:
        sql = "SELECT * FROM observations WHERE project_id = ?"
        args: list[object] = [project_id]
        if start:
            sql += " AND observed_at >= ?"
            args.append(start.isoformat())
        if end:
            sql += " AND observed_at <= ?"
            args.append(end.isoformat())
        sql += " ORDER BY observed_at ASC"
        with self._connect() as db:
            rows = db.execute(sql, args).fetchall()
        return [dict(row) for row in rows]
