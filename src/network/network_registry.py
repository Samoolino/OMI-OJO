"""Chain-agnostic network registry and deterministic anchor contracts."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class NetworkEnvironment(StrEnum):
    DESIGN = "DESIGNED"
    TESTNET = "TESTNET"
    CONTROLLED_TEST = "CONTROLLED_TEST"
    INTEGRATION_READY = "INTEGRATION_READY"
    PRODUCTION_APPROVED = "PRODUCTION_APPROVED"


@dataclass(frozen=True)
class NetworkDefinition:
    network_id: str
    name: str
    environment: NetworkEnvironment
    chain_id: str | None
    network_type: str
    anchor_contract: str | None
    contract_version: str | None
    deployment_revision: str | None
    status: str


@dataclass(frozen=True)
class AnchorRecord:
    anchor_id: str
    evidence_package_id: str
    snapshot_id: str
    root_hash: str
    network_id: str
    contract_version: str
    transaction_id: str | None
    anchored_at: str | None
    verification_status: str


class NetworkRegistry:
    """In-memory reference registry; persistence is intentionally injected later."""

    def __init__(self, networks: tuple[NetworkDefinition, ...] = ()) -> None:
        self._networks = {network.network_id: network for network in networks}

    def register(self, network: NetworkDefinition) -> None:
        if network.network_id in self._networks:
            raise ValueError(f"network already registered: {network.network_id}")
        self._networks[network.network_id] = network

    def get(self, network_id: str) -> NetworkDefinition:
        try:
            return self._networks[network_id]
        except KeyError as exc:
            raise KeyError(f"unknown network: {network_id}") from exc

    def list(self) -> tuple[NetworkDefinition, ...]:
        return tuple(self._networks[key] for key in sorted(self._networks))


class AnchorAdapter:
    """Minimal chain-neutral contract implemented by each network adapter."""

    def create_anchor(self, *, root_hash: str, snapshot_id: str, metadata_reference: str) -> AnchorRecord:
        raise NotImplementedError

    def get_anchor(self, anchor_id: str) -> AnchorRecord:
        raise NotImplementedError

    def verify_anchor(self, *, anchor_id: str, root_hash: str) -> bool:
        raise NotImplementedError
