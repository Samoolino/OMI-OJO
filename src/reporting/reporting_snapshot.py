"""Canonical reporting snapshot/read-model builder for OMI-OJO."""
from __future__ import annotations
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib, json
from typing import Iterable
from .reportable_data import Observation, ReportabilityDecision, ReportabilityState
@dataclass(frozen=True)
class ReportingSnapshot:
    schema_version:str; snapshot_id:str; created_at:str; reporting_period_start:str; reporting_period_end:str
    project_id:str; site_ids:tuple[str,...]; report_family:str; reportable_observation_ids:tuple[str,...]
    contextual_observation_ids:tuple[str,...]; excluded_observation_ids:tuple[str,...]; indicator_ids:tuple[str,...]
    source_ids:tuple[str,...]; evidence_package_id:str|None; methodology_versions:tuple[str,...]
    configuration_revision:str; release_state:str; deterministic_hash:str
def build_snapshot(*,project_id:str,report_family:str,period_start:datetime,period_end:datetime,
 observations:Iterable[Observation],decisions:Iterable[ReportabilityDecision],release_state:str="DRAFT",
 evidence_package_id:str|None=None,methodology_versions:Iterable[str]=(),configuration_revision:str="UNSET")->ReportingSnapshot:
 idx={o.observation_id:o for o in observations}; ds=list(decisions)
 reportable=tuple(sorted(d.observation_id for d in ds if d.state==ReportabilityState.REPORTABLE))
 contextual=tuple(sorted(d.observation_id for d in ds if d.state==ReportabilityState.CONTEXTUAL_ONLY))
 excluded=tuple(sorted(d.observation_id for d in ds if d.state not in {ReportabilityState.REPORTABLE,ReportabilityState.CONTEXTUAL_ONLY}))
 inc=[idx[i] for i in reportable+contextual if i in idx]; sites=tuple(sorted({o.site_id for o in inc}))
 inds=tuple(sorted({o.indicator_id for o in inc})); sources=tuple(sorted({o.source_id for o in inc})); methods=tuple(sorted(set(methodology_versions)))
 canonical={"schema_version":"UB-02.REPORTING-SNAPSHOT.2","project_id":project_id,"report_family":report_family,
 "period_start":period_start.astimezone(timezone.utc).isoformat(),"period_end":period_end.astimezone(timezone.utc).isoformat(),
 "reportable":reportable,"contextual":contextual,"excluded":excluded,"sites":sites,"indicators":inds,"sources":sources,
 "evidence_package_id":evidence_package_id,"methodology_versions":methods,"configuration_revision":configuration_revision,"release_state":release_state}
 digest=hashlib.sha256(json.dumps(canonical,sort_keys=True,separators=(",",":")).encode()).hexdigest()
 return ReportingSnapshot(canonical["schema_version"],f"RS-{digest[:16]}",datetime.now(timezone.utc).isoformat(),
 canonical["period_start"],canonical["period_end"],project_id,sites,report_family,reportable,contextual,excluded,inds,sources,
 evidence_package_id,methods,configuration_revision,release_state,digest)
def snapshot_to_dict(snapshot:ReportingSnapshot)->dict[str,object]: return asdict(snapshot)
