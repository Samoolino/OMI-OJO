from __future__ import annotations
from dataclasses import dataclass
import hashlib,json
from src.grants.s6b_evidence_manifest import EvidenceManifestItem,build_s6b_manifest
from src.reporting.release_governance import ReleaseDecision,ReleaseState
@dataclass(frozen=True)
class InstitutionalEvidenceArtifact:
    artifact_type:str; project_id:str; snapshot_id:str; evidence_package_id:str; release_id:str; release_state:str; configuration_revision:str; deterministic_hash:str
def build_grant_evidence_artifact(*,project_id:str,release:ReleaseDecision,artifacts:list[EvidenceManifestItem])->InstitutionalEvidenceArtifact:
    if release.state!=ReleaseState.RELEASED: raise ValueError('institutional_artifact_requires_released_snapshot')
    m=build_s6b_manifest(project_id=project_id,snapshot_id=release.snapshot_id,evidence_package_id=release.evidence_package_id,release_state=release.state.value,configuration_revision=release.configuration_revision,artifacts=artifacts)
    p={'artifact_type':'GRANT_EVIDENCE','project_id':project_id,'snapshot_id':release.snapshot_id,'evidence_package_id':release.evidence_package_id,'release_id':release.release_id,'release_state':release.state.value,'configuration_revision':release.configuration_revision,'manifest_hash':m.deterministic_hash}
    d=hashlib.sha256(json.dumps(p,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return InstitutionalEvidenceArtifact(**p,deterministic_hash=d)
