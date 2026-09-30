from src.grants.released_evidence_artifact import build_grant_evidence_artifact
from src.grants.s6b_evidence_manifest import EvidenceManifestItem
from src.reporting.release_governance import ReleaseState,create_release,transition_release
from src.vdr.evidence_manifest import build_vdr_manifest

def _released():
    r=create_release(snapshot_id='RS-1',evidence_package_id='EP-1',snapshot_hash='a'*64,configuration_revision='git:test',policy_revision='policy:test')
    r=transition_release(r,ReleaseState.REVIEW)
    r=transition_release(r,ReleaseState.APPROVED,reviewer='reviewer')
    return transition_release(r,ReleaseState.RELEASED,reviewer='authority')

def test_grant_and_vdr_share_release():
    r=_released(); items=(EvidenceManifestItem('ep','evidence','evidence.json'),)
    g=build_grant_evidence_artifact(project_id='S6C',release=r,artifacts=list(items))
    v=build_vdr_manifest(organization_id='ORG-1',project_id='S6C',release=r,claim_ids=('CLM-1',),artifacts=items)
    assert g.snapshot_id==v.snapshot_id==r.snapshot_id
    assert g.evidence_package_id==v.evidence_package_id==r.evidence_package_id
