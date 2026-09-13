"""Canonical evidence hashing and bottle/seal identity."""
import hashlib
import json
from dataclasses import dataclass
from typing import Any


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_hex(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


@dataclass(frozen=True)
class BottleIdentity:
    bottle_id: str
    batch_id: str
    seal_id: str
    evidence_hash: str


def create_bottle_identity(bottle_id: str, batch_id: str, seal_id: str, evidence: dict[str, Any]) -> BottleIdentity:
    if not bottle_id or not batch_id or not seal_id:
        raise ValueError("bottle, batch and seal identifiers are required")
    return BottleIdentity(bottle_id, batch_id, seal_id, sha256_hex(evidence))
