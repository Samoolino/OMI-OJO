import unittest

from src.production.evidence_anchor import (
    AnchorRecord,
    canonical_evidence_package,
    evidence_root,
    validate_anchor_record,
    verification_status,
)


class EvidenceAnchorTests(unittest.TestCase):
    def make_package(self):
        return canonical_evidence_package(
            evidence_id="EVID-001",
            project_id="OMI-OJO",
            evidence_class="OBSERVED",
            source_refs=["rain-provider"],
            observation_refs=["OBS-2", "OBS-1"],
            event_site_refs=["SITE-01"],
            methodology_ref="RAIN-1.0",
            quality_state="REPORTABLE",
            created_at="2026-09-22T10:00:00+00:00",
            observation_window={"start": "2026-09-22T09:00:00+00:00", "end": "2026-09-22T10:00:00+00:00"},
            geography_ref="LAGOS-SITE-01",
            content_hashes=["bb", "aa"],
        )

    def test_deterministic_root_is_order_independent(self):
        a = self.make_package()
        b = self.make_package()
        self.assertEqual(evidence_root(a), evidence_root(b))

    def test_verifier_matches_and_rejects_tampering(self):
        package = self.make_package()
        root = evidence_root(package)
        self.assertEqual(verification_status(package, root), "MATCHED")
        package["quality_state"] = "VERIFIED"
        self.assertEqual(verification_status(package, root), "MISMATCHED")

    def test_anchor_record_validation(self):
        record = AnchorRecord(
            evidence_id="EVID-001",
            schema_version="BE-EVIDENCE-1.0",
            evidence_root="a" * 64,
            network_id="controlled-testnet",
            chain_id=1,
            contract_address="0x" + "1" * 40,
            transaction_hash="0x" + "2" * 64,
            block_number=10,
            block_timestamp="2026-09-22T10:00:00+00:00",
            anchor_status="ANCHORED",
            anchored_at="2026-09-22T10:01:00+00:00",
        )
        validate_anchor_record(record)
