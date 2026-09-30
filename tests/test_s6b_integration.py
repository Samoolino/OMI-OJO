from src.grants.s6b_evidence_manifest import EvidenceManifestItem, build_s6b_manifest
from src.network.anchor_verifier import VerificationState, verify_anchor_root


def test_s6b_manifest_is_deterministic():
    items = [
        EvidenceManifestItem("test-2", "deployment", "receipt.json"),
        EvidenceManifestItem("test-1", "architecture", "architecture.md"),
    ]
    a = build_s6b_manifest(
        project_id="S6B-DEMO",
        snapshot_id="RS-1",
        evidence_package_id="EP-1",
        release_state="REVIEW",
        configuration_revision="git:abc",
        artifacts=items,
    )
    b = build_s6b_manifest(
        project_id="S6B-DEMO",
        snapshot_id="RS-1",
        evidence_package_id="EP-1",
        release_state="REVIEW",
        configuration_revision="git:abc",
        artifacts=list(reversed(items)),
    )
    assert a.deterministic_hash == b.deterministic_hash
    assert [i.artifact_id for i in a.items] == ["test-1", "test-2"]


def test_anchor_verification_has_required_public_states():
    assert verify_anchor_root(anchor=None, expected_root="abc").state == VerificationState.NOT_FOUND
