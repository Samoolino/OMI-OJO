from src.network.anchor_registry import AnchorRegistry
from src.network.integrity_anchor_service import AnchorRequest, InMemoryAnchorAdapter, IntegrityAnchorService


def test_anchor_service_persists_and_verifies_root(tmp_path):
    registry = AnchorRegistry(str(tmp_path / "anchors.db"))
    adapter = InMemoryAnchorAdapter()
    service = IntegrityAnchorService(registry, {"builder-testnet": adapter})

    request = AnchorRequest(
        evidence_package_id="EP-001",
        snapshot_id="RS-001",
        root_hash="a" * 64,
        network_id="builder-testnet",
        contract_id="integrity-anchor-v1",
        contract_version="1.0.0",
    )

    record = service.anchor(request)
    assert registry.get(record.anchor_id) == record
    assert service.verify(record.anchor_id, "a" * 64) == "MATCHED"
    assert service.verify(record.anchor_id, "b" * 64) == "MISMATCHED"
    assert service.verify("AN-missing", "a" * 64) == "NOT_FOUND"
