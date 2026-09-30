"""Canonical governed refresh pipeline."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime,timezone
from typing import Callable,Iterable
from .agentic_collection import CollectionRun,process_collection_evidence
from .engagement_orchestrator import OrchestrationPlan,ingest_plan
from .observation_store import ObservationStore
from .refresh_policy import RefreshPolicy,next_refresh
from .reportable_data import Observation,ReportingRule,evaluate_batch
from .reporting_snapshot import build_snapshot
from .snapshot_store import SnapshotStore
@dataclass(frozen=True)
class RefreshResult:
 engagement_id:str; project_id:str; report_family:str; ingested:int; decisions:int; snapshot_id:str; snapshot_hash:str; next_refresh_at:str|None; evidence_package_id:str|None=None; qc_decisions:int=0
def run_refresh(*,policy:RefreshPolicy,project_id:str,report_family:str,period_start:datetime,period_end:datetime,observations:Iterable[Observation],rules:Iterable[ReportingRule],observation_store:ObservationStore,snapshot_store:SnapshotStore,now:datetime|None=None,approved_sources:frozenset[str]|None=None,evidence_location:tuple[float,float]|None=None,configuration_revision:str="UNSET")->RefreshResult:
 current=now or datetime.now(timezone.utc); items=tuple(observations); rs=tuple(rules); approved=approved_sources or frozenset(s for r in rs for s in r.allowed_sources)
 ev=process_collection_evidence(collection=CollectionRun(actions=tuple(),observations=items,skipped=tuple()),approved_sources=approved,now=current,location=evidence_location)
 dec=evaluate_batch(ev.reportable_observations,rs,now=current); persisted=observation_store.upsert(ev.reportable_observations)
 snap=build_snapshot(project_id=project_id,report_family=report_family,period_start=period_start,period_end=period_end,observations=ev.reportable_observations,decisions=dec,release_state="DRAFT",evidence_package_id=ev.package.package_id,methodology_versions=ev.package.methodology,configuration_revision=configuration_revision)
 snapshot_store.save(snap); nxt=next_refresh(current,policy)
 return RefreshResult(policy.engagement_id,project_id,report_family,persisted,len(dec),snap.snapshot_id,snap.deterministic_hash,nxt.isoformat() if nxt else None,ev.package.package_id,len(ev.qc_decisions))
def run_orchestrated_refresh(*,plan:OrchestrationPlan,policy:RefreshPolicy,report_family:str,period_start:datetime,period_end:datetime,observation_store:ObservationStore,snapshot_store:SnapshotStore,now:datetime|None=None,configuration_revision:str="UNSET")->RefreshResult:
 obs,_=ingest_plan(plan); return run_refresh(policy=policy,project_id=plan.project_id,report_family=report_family,period_start=period_start,period_end=period_end,observations=obs,rules=plan.rules,observation_store=observation_store,snapshot_store=snapshot_store,now=now,approved_sources=frozenset(s for r in plan.rules for s in r.allowed_sources),configuration_revision=configuration_revision)
def run_due_engagements(*,policies:Iterable[RefreshPolicy],last_refresh:dict[str,datetime],refreshers:dict[str,Callable[[],RefreshResult]],now:datetime|None=None)->list[RefreshResult]:
 current=now or datetime.now(timezone.utc); out=[]
 for p in policies:
  prev=last_refresh.get(p.engagement_id)
  if p.enabled and (prev is None or current>=next_refresh(prev,p)) and p.engagement_id in refreshers: out.append(refreshers[p.engagement_id]())
 return out
