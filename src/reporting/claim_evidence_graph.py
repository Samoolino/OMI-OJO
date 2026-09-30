"""Claim-to-evidence graph for reporting, grant and VDR traceability."""
from __future__ import annotations
from dataclasses import dataclass
from enum import StrEnum
import hashlib,json
from typing import Iterable
class ClaimState(StrEnum): DRAFT="DRAFT"; SUPPORTED="SUPPORTED"; BLOCKED="BLOCKED"; RELEASED="RELEASED"
@dataclass(frozen=True)
class EvidenceLink: claim_id:str; observation_ids:tuple[str,...]; evidence_package_id:str; snapshot_id:str; methodology_version:str; source_ids:tuple[str,...]
@dataclass(frozen=True)
class Claim: claim_id:str; project_id:str; statement:str; indicator_id:str; state:ClaimState; evidence:EvidenceLink; deterministic_hash:str
def build_claim(*,project_id:str,statement:str,indicator_id:str,observation_ids:Iterable[str],evidence_package_id:str,snapshot_id:str,methodology_version:str,source_ids:Iterable[str],state:ClaimState=ClaimState.DRAFT)->Claim:
 obs=tuple(sorted(observation_ids)); src=tuple(sorted(source_ids)); canonical={"project_id":project_id,"statement":statement,"indicator_id":indicator_id,"state":state.value,"observation_ids":obs,"evidence_package_id":evidence_package_id,"snapshot_id":snapshot_id,"methodology_version":methodology_version,"source_ids":src}
 digest=hashlib.sha256(json.dumps(canonical,sort_keys=True,separators=(",",":")).encode()).hexdigest(); cid=f"CLM-{digest[:16]}"
 return Claim(cid,project_id,statement,indicator_id,state,EvidenceLink(cid,obs,evidence_package_id,snapshot_id,methodology_version,src),digest)
def validate_claim_against_snapshot(claim:Claim,snapshot:object,*,evidence_package_id:str)->None:
 if claim.evidence.snapshot_id!=getattr(snapshot,"snapshot_id"): raise ValueError("claim_snapshot_mismatch")
 if claim.evidence.evidence_package_id!=evidence_package_id: raise ValueError("claim_evidence_package_mismatch")
 if claim.project_id!=getattr(snapshot,"project_id"): raise ValueError("claim_project_mismatch")
 allowed=set(getattr(snapshot,"reportable_observation_ids"))|set(getattr(snapshot,"contextual_observation_ids"))
 if not set(claim.evidence.observation_ids).issubset(allowed): raise ValueError("claim_observation_not_in_snapshot")
