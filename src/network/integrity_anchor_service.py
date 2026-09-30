"""Chain-neutral integrity anchoring orchestration.

The service anchors deterministic evidence roots only. It never interprets an
anchor as environmental verification.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Protocol

from .anchor_registry import AnchorRecord, AnchorRegistry


@dataclass(frozen=True)
class AnchorRequest:
    evidence_package_id: str
    snapshot_id: str
    root_hash: str
    network_id: str
    contract_id: str
    contract_version: str


@dataclass(frozen=True)
class AnchorReceipt:
    transaction_id: str
    anchored_at: datetime
    root_hash: str
    network_id: str
    contract_id: str
    contract_version: str


class AnchorAdapter(Protocol):
    def create_anchor(self, request: AnchorRequest) -> AnchorReceipt: ...
    def get_anchor(self, transaction_id: str) -> AnchorReceipt | None: ...


class IntegrityAnchorService:
    def __init__(self, registry: AnchorRegistry, adapters: dict[str, AnchorAdapter]) -> None:
        self.registry = registry
        self.adapters = adapters

    def anchor(self, request: AnchorRequest) -> AnchorRecord:
        adapter = self.adapters.get(request.network_id)
        if adapter is None:
            raise ValueError(f"network adapter not registered: {request.network_id}")

        receipt = adapter.create_anchor(request)
        if receipt.root_hash != request.root_hash:
            raise ValueError("anchor adapter returned a mismatched root hash")

        record = AnchorRecord(
            anchor_id=f"AN-{receipt.transaction_id}",
            evidence_package_id=request.evidence_package_id,
            snapshot_id=request.snapshot_id,
            root_hash=request.root_hash,
            network_id=receipt.network_id,
            contract_id=receipt.contract_id,
            contract_version=receipt.contract_version,
            transaction_id=receipt.transaction_id,
            anchored_at=receipt.anchored_at.isoformat(),
            verification_status="ANCHORED",
        )
        self.registry.save(record)
        return record

    def verify(self, anchor_id: str, expected_root_hash: str) -> str:
        record = self.registry.get(anchor_id)
        if record is None:
            return "NOT_FOUND"
        return "MATCHED" if record.root_hash == expected_root_hash else "MISMATCHED"


class InMemoryAnchorAdapter:
    """Deterministic test adapter; not a production blockchain connector."""

    def __init__(self) -> None:
        self._receipts: dict[str, AnchorReceipt] = {}

    def create_anchor(self, request: AnchorRequest) -> AnchorReceipt:
        transaction_id = f"testnet-{request.root_hash[:24]}"
        receipt = AnchorReceipt(
            transaction_id=transaction_id,
            anchored_at=datetime.now(timezone.utc),
            root_hash=request.root_hash,
            network_id=request.network_id,
            contract_id=request.contract_id,
            contract_version=request.contract_version,
        )
        self._receipts[transaction_id] = receipt
        return receipt

    def get_anchor(self, transaction_id: str) -> AnchorReceipt | None:
        return self._receipts.get(transaction_id)
