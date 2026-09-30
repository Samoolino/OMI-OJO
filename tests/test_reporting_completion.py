from datetime import datetime,timezone
from src.reporting.claim_evidence_graph import build_claim,validate_claim_against_snapshot
from src.reporting.release_governance import ReleaseState,create_release
from src.reporting.release_store import ReleaseStore
from src.reporting.reporting_snapshot import build_snapshot
from src.reporting.reportable_data import EvidenceClass,Location,Observation,ReportabilityDecision,ReportabilityState
def test_snapshot_claim_release(tmp_path):
 o=Observation("OBS-1","S6C","lagos-s6c","rainfall",datetime(2026,9,30,10,tzinfo=timezone.utc),Location(6.4,3.5),"12","mm","open-meteo-forecast",EvidenceClass.CONTEXTUAL,True,{"provider":"open-meteo","source_snapshot_id":"snap-1","methodology_status":"registered"})
 d=ReportabilityDecision("OBS-1",ReportabilityState.REPORTABLE,("ok",))
 s=build_snapshot(project_id="S6C",report_family="CLIMATE",period_start=o.observed_at,period_end=o.observed_at,observations=[o],decisions=[d],evidence_package_id="EP-1",methodology_versions=["provider_provenance_checked"],configuration_revision="git:test")
 c=build_claim(project_id="S6C",statement="Rainfall context",indicator_id="rainfall",observation_ids=["OBS-1"],evidence_package_id="EP-1",snapshot_id=s.snapshot_id,methodology_version="provider_provenance_checked",source_ids=["open-meteo-forecast"])
 validate_claim_against_snapshot(c,s,evidence_package_id="EP-1")
 r=create_release(snapshot_id=s.snapshot_id,evidence_package_id="EP-1",snapshot_hash=s.deterministic_hash,configuration_revision=s.configuration_revision,policy_revision="policy:test")
 store=ReleaseStore(str(tmp_path/"release.db")); assert store.save(r)
 r=store.transition(r,ReleaseState.REVIEW); r=store.transition(r,ReleaseState.APPROVED,reviewer="reviewer"); r=store.transition(r,ReleaseState.RELEASED,reviewer="release-authority")
 assert store.latest(s.snapshot_id)["state"]=="RELEASED"
