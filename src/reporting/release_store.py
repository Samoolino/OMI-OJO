from __future__ import annotations
import json,sqlite3
from dataclasses import asdict
from pathlib import Path
from .release_governance import ReleaseDecision,ReleaseState
class ReleaseStore:
 def __init__(self,path:str="data/reporting/releases.db")->None:
  self.path=path; Path(path).parent.mkdir(parents=True,exist_ok=True)
  with sqlite3.connect(path) as db:
   db.execute("CREATE TABLE IF NOT EXISTS release_decisions (decision_id TEXT PRIMARY KEY,snapshot_id TEXT NOT NULL,evidence_package_id TEXT NOT NULL,state TEXT NOT NULL,decision_hash TEXT NOT NULL,decided_at TEXT NOT NULL,payload_json TEXT NOT NULL)")
   db.execute("CREATE INDEX IF NOT EXISTS idx_release_snapshot ON release_decisions(snapshot_id, decided_at)"); db.commit()
 def save(self,decision:ReleaseDecision)->bool:
  payload=json.dumps(asdict(decision),sort_keys=True,separators=(",",":"))
  with sqlite3.connect(self.path) as db:
   cur=db.execute("INSERT OR IGNORE INTO release_decisions VALUES (?,?,?,?,?,?,?)",(decision.release_id,decision.snapshot_id,decision.evidence_package_id,decision.state.value,decision.deterministic_hash,decision.decided_at,payload)); db.commit(); return cur.rowcount==1
 def transition(self,decision:ReleaseDecision,target:ReleaseState,*,reviewer:str|None=None,reason:str|None=None)->ReleaseDecision:
  from .release_governance import transition_release
  nxt=transition_release(decision,target,reviewer=reviewer,reason=reason); self.save(nxt); return nxt
 def history(self,snapshot_id:str,limit:int=50)->list[dict]:
  with sqlite3.connect(self.path) as db: rows=db.execute("SELECT payload_json FROM release_decisions WHERE snapshot_id=? ORDER BY decided_at ASC LIMIT ?",(snapshot_id,limit)).fetchall()
  return [json.loads(r[0]) for r in rows]
 def latest(self,snapshot_id:str)->dict|None:
  h=self.history(snapshot_id,1000000); return h[-1] if h else None
