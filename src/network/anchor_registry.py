"""Persistent integrity-anchor records, independent of a specific chain."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
import sqlite3
from pathlib import Path


@dataclass(frozen=True)
class AnchorRecord:
    anchor_id: str
    evidence_package_id: str
    snapshot_id: str
    root_hash: str
    network_id: str
    contract_id: str
    contract_version: str
    transaction_id: str | None
    anchored_at: str | None
    verification_status: str


class AnchorRegistry:
    def __init__(self, path: str = "data/network/anchors.db") -> None:
        self.path = path
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(path) as db:
            db.execute("""CREATE TABLE IF NOT EXISTS anchors (
                anchor_id TEXT PRIMARY KEY,
                snapshot_id TEXT NOT NULL,
                evidence_package_id TEXT NOT NULL,
                root_hash TEXT NOT NULL,
                network_id TEXT NOT NULL,
                payload_json TEXT NOT NULL
            )""")
            db.commit()

    def save(self, record: AnchorRecord) -> None:
        payload = json.dumps(asdict(record), sort_keys=True, separators=(",", ":"))
        with sqlite3.connect(self.path) as db:
            db.execute("INSERT OR REPLACE INTO anchors VALUES (?, ?, ?, ?, ?, ?)", (
                record.anchor_id, record.snapshot_id, record.evidence_package_id,
                record.root_hash, record.network_id, payload,
            ))
            db.commit()

    def get(self, anchor_id: str) -> AnchorRecord | None:
        with sqlite3.connect(self.path) as db:
            row = db.execute("SELECT payload_json FROM anchors WHERE anchor_id = ?", (anchor_id,)).fetchone()
        return AnchorRecord(**json.loads(row[0])) if row else None
