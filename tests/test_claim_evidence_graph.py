from src.reporting.claim_evidence_graph import ClaimState, build_claim


def test_claim_is_deterministic_and_binds_evidence():
    kwargs = dict(
        project_id="S5-GLOBAL-LAGOS",
        statement="Rainfall observation is supported by the governed evidence snapshot.",
        indicator_id="rainfall",
        observation_ids=["obs-2", "obs-1"],
        evidence_package_id="EP-abc",
        snapshot_id="RS-abc",
        methodology_version="rainfall.v1",
        source_ids=["open-meteo-forecast"],
        state=ClaimState.SUPPORTED,
    )
    a = build_claim(**kwargs)
    b = build_claim(**kwargs)
    assert a.claim_id == b.claim_id
    assert a.deterministic_hash == b.deterministic_hash
    assert a.evidence.claim_id == a.claim_id
    assert a.evidence.observation_ids == ("obs-1", "obs-2")
