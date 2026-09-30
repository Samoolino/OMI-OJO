from __future__ import annotations
from dataclasses import dataclass
import hashlib,json
from src.grants.s6b_evidence_manifest import EvidenceManifestItem
from src.reporting.release_governance import ReleaseDecision,ReleaseState
@dataclass(frozen=True)
class VDREvidenceManifest:
    organization_id:str; project_id:str; snapshot_id:str; evidence_package_id:str; release_id:str; release_state:str; claim_ids:tuple[str,...]; artifact_ids:tuple[str,...]; configuration_revision:str; deterministic_hash:str
def build_vdr_manifest(*,organization_id:str,project_id:str,release:ReleaseDecision,claim_ids:tuple[str,...],artifacts:tuple[EvidenceManifestItem,...])->VDREvidenceManifest:
    if release.state!=ReleaseState.RELEASED: raise ValueError('vdr_manifest_requires_released_snapshot')
    canonical={'organization_id':organization_id,'project_id':project_id,'snapshot_id':release.snapshot_id,'evidence_package_id':release.evidence_package_id,'release_id':release.release_id,'release_state':release.state.value,'claim_ids':tuple(sorted(claim_ids)),'artifact_ids':tuple(sorted(a.artifact_id for a in artifacts)),'configuration_revision':release.configuration_revision}
    digest=hashlib.sha256(json.dumps(canonical,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return VDREvidenceManifest(**canonical,deterministic_hash=digest)
