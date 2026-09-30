export default function FirstLiveHarvestPage() {
  const gates = [
    ["S13.1","ACTIVATION READINESS","READY FOR ACTUAL EVENT INPUT"],
    ["S13.2","RAIN EVENT + PRE-EVENT SITE CHECK","READY FOR ACTUAL EVENT INPUT"],
    ["S13.3","FIRST-FLUSH DIVERSION","READY FOR ACTUAL EVENT INPUT"],
    ["S13.4","CONTROLLED COLLECTION","READY FOR ACTUAL EVENT INPUT"],
    ["S13.5","LIVE MEASUREMENT + VIDEO","READY FOR ACTUAL EVENT INPUT"],
    ["S13.6","SAMPLE + CUSTODY","READY FOR ACTUAL EVENT INPUT"],
    ["S13.7","QMS / LAB HANDOFF","READY FOR ACTUAL EVENT INPUT"],
    ["S13.8","BATCH + SEAL","READY FOR ACTUAL EVENT INPUT"],
    ["S13.9","DMRV EVENT PACKAGE","READY FOR ACTUAL EVENT INPUT"],
    ["S13.10","EVIDENCE RECONCILIATION","READY FOR ACTUAL EVENT INPUT"],
    ["S13.11","ANCHOR CANDIDATE","READY FOR ACTUAL EVENT INPUT"],
    ["S13.12","EXTERNAL ASSURANCE REVIEW","PENDING S13.11"],
    ["S13.13","PREMIUM-CONDITION DECISION","PENDING"],
    ["S13.14","REGULATORY / PRODUCT RELEASE GATE","PENDING"]
  ];
  const controls = [
    "S13.10 reconciliation complete within defined scope",
    "Material reconciliation exceptions resolved or dispositioned",
    "Locked DMRV package digest and version",
    "Anchor scope and event identifier frozen",
    "Anchor schema/methodology versions registered",
    "Network and evidence-anchor registry target identified",
    "Candidate digest and package lineage validated",
    "Candidate construction identity and timestamp recorded",
    "No transaction hash/block confirmation represented unless actually executed"
  ];
  return (
    <main style={{maxWidth:1120,margin:"0 auto",padding:"48px 24px",fontFamily:"Arial,sans-serif"}}>
      <header style={{borderBottom:"1px solid #ddd",paddingBottom:24}}>
        <p style={{fontSize:13,letterSpacing:1.5,fontWeight:700}}>S13 · EMPIRICAL EVENT CONTROL</p>
        <h1 style={{fontSize:40,margin:"8px 0"}}>First Live Harvest & Evidence Event</h1>
        <p style={{fontSize:18,lineHeight:1.6,maxWidth:850}}>Controlled pathway for the first actual authorized field event. The repository does not assert that an event has occurred.</p>
        <div style={{display:"flex",gap:10,flexWrap:"wrap"}}><Badge>NO LIVE EVENT CLAIMED</Badge><Badge>PHYSICAL PRODUCTION NOT RELEASED</Badge><Badge>FAIL-CLOSED</Badge></div>
      </header>
      <section style={{marginTop:28,padding:22,border:"1px solid #ddd",borderRadius:12}}>
        <h2 style={{marginTop:0}}>S13.11 blockchain anchor candidate gate</h2>
        <p style={{lineHeight:1.6}}>A deterministic candidate may be prepared only from a reconciled, locked package. Candidate construction is not a blockchain transaction and does not verify environmental truth.</p>
        <ul>{controls.map(c=><li key={c} style={{margin:"9px 0"}}>{c}</li>)}</ul>
      </section>
      <section style={{marginTop:32}}><h2>Controlled gates</h2><div style={{display:"grid",gap:10}}>{gates.map(([id,name,state])=><div key={id} style={{display:"grid",gridTemplateColumns:"80px 1fr auto",gap:12,alignItems:"center",padding:14,border:"1px solid #ddd",borderRadius:9}}><strong>{id}</strong><span>{name}</span><small>{state}</small></div>)}</div></section>
      <section style={{marginTop:32,padding:20,background:"#f7f7f7",borderRadius:12}}><h2>Evidence boundary</h2><p style={{lineHeight:1.6}}>An anchor candidate is an integrity/reference artifact. It does not establish environmental truth, certification, premium condition or product release. No transaction hash or block confirmation is claimed here.</p></section>
    </main>
  );
}
function Badge({children}:{children:React.ReactNode}) { return <span style={{fontSize:12,fontWeight:700,padding:"7px 10px",border:"1px solid #bbb",borderRadius:999}}>{children}</span>; }
