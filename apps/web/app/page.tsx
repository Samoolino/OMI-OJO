"use client";

import { useState } from "react";
import WebGLGlobe from "./components/WebGLGlobe";

const nav=["Command Center","Harvest Intelligence","Evidence & DMRV","ESG / GHG","Investor Room"];
const gates=["Source registry","Forecast snapshot","Measured telemetry","Rain event","Collection + first flush","Water/QMS","Batch + bottle seal","Evidence root","DMRV review","Blockchain proof"];
const batches=[
  {id:"BE-OMI-0001",site:"Pilot Catchment A",status:"VERIFIED",volume:"—",evidence:"Pending empirical evidence"},
  {id:"BE-OMI-0002",site:"Pilot Catchment B",status:"PENDING",volume:"—",evidence:"Awaiting measured telemetry"},
  {id:"BE-OMI-0003",site:"Controlled scenario",status:"SIMULATED",volume:"400 L model",evidence:"Model only; not production"}
];

export default function Home(){
  const [active,setActive]=useState("Command Center");
  const [demo,setDemo]=useState(false);
  return <div className="shell">
    <header className="topbar"><div className="brand"><div className="mark">B</div><div>BLUE-ETHER <span style={{color:"#6a968a"}}>OS</span></div></div><div className="status">M-1 · S4 GATED · EVIDENCE-FIRST</div></header>
    <div className="layout">
      <aside className="nav">{nav.map(n=><button key={n} className={active===n?"active":""} onClick={()=>setActive(n)}>{n}</button>)}</aside>
      <main className="main">
        <section className="hero">
          <div className="panel hero-copy"><div className="eyebrow">37-LCDA Water + Environmental Data Operating System</div><h1>Rain becomes an investable evidence stream.</h1><p>Predict rainfall. Plan collection. Prove water quality. Trace every bottle. Build DMRV-grade ESG evidence without confusing forecasts, models or simulations with measured production.</p><div className="actions"><button className="primary" onClick={()=>setDemo(!demo)}>{demo?"Hide scenario":"Run controlled scenario"}</button><button className="secondary" onClick={()=>setActive("Investor Room")}>Open investor room</button></div>{demo&&<div style={{marginTop:16,color:"#a7f3d0",fontSize:13}}>CONTROLLED SIMULATION · Forecast → event → collection → QMS → batch → seal → hash → verify. No live production claim.</div>}</div>
          <div className="panel globe"><WebGLGlobe/><div className="globe-overlay"><div><span className="badge verified">WEBGL · LIVE INTERACTION</span></div><div><strong>Rainfall intelligence surface</strong><div className="muted">Spatial context is visualization; evidence status remains authoritative.</div></div></div></div>
        </section>
        <section className="metric-grid">
          <div className="panel metric"><div className="label">Evidence maturity</div><div className="value">S3</div><div className="delta">S4 gated · fail closed</div></div>
          <div className="panel metric"><div className="label">Production chain</div><div className="value">14/17</div><div className="delta">Repository gates implemented</div></div>
          <div className="panel metric"><div className="label">Claim integrity</div><div className="value">100%</div><div className="delta">Forecast ≠ measured</div></div>
          <div className="panel metric"><div className="label">Bankable yield</div><div className="value">—</div><div className="delta">Empirical validation required</div></div>
        </section>
        <section className="grid">
          <div className="panel section"><h2>{active}</h2><div className="muted">Institutional control surface · status-aware by design</div>
            {active==="Command Center"&&<><div className="timeline">{gates.map((g,i)=><div className="step" key={g}><span className={i<8?"dot":"dot pending"}></span><div style={{flex:1}}><strong>{g}</strong><div className="muted">{i<8?"Core boundary implemented":"Review / external evidence required"}</div></div><span className={i<8?"badge verified":"badge pending-b"}>{i<8?"IMPLEMENTED":"PENDING"}</span></div>)}</div></>}
            {active==="Harvest Intelligence"&&<div className="cards"><div className="mini"><strong>Forecast</strong><span>Immutable snapshots with provider, retrieval time, location and provenance.</span></div><div className="mini"><strong>Reconciliation</strong><span>Measured observations remain distinct and can be compared against hourly forecast values.</span></div><div className="mini"><strong>Capacity</strong><span>Catchment × rainfall × runoff × collection efficiency feeds planning; model status is explicit.</span></div></div>}
            {active==="Evidence & DMRV"&&<div className="cards"><div className="mini"><strong>Evidence root</strong><span>Canonical payloads and SHA-256 hashes provide deterministic evidence identity.</span></div><div className="mini"><strong>DMRV lifecycle</strong><span>RAW → INGESTED → QUALITY_CHECKED → VALIDATED → PACKAGED → REVIEWED.</span></div><div className="mini"><strong>Verifier</strong><span>Bottle → batch → evidence root → proof, with confidential operational data excluded.</span></div></div>}
            {active==="ESG / GHG"&&<div className="cards"><div className="mini"><strong>ESG</strong><span>Environmental, social, governance plus economic and regulatory indicators.</span></div><div className="mini"><strong>GHG</strong><span>Activity data, emission factor, scope, methodology, uncertainty and status are mandatory.</span></div><div className="mini"><strong>Carbon adapter</strong><span>Designed for optional Climatiq integration; API credentials and factor selection remain external controls.</span></div></div>}
            {active==="Investor Room"&&<><div className="cards"><div className="mini"><strong>Technical diligence</strong><span>Architecture, tests, release sequence, threat boundaries and evidence contracts.</span></div><div className="mini"><strong>Operational diligence</strong><span>Rainfall, instruments, collection, QMS, bottling and site evidence.</span></div><div className="mini"><strong>Impact diligence</strong><span>ESG/GHG methodology, assumptions, uncertainty and verification pathway.</span></div></div><div className="bar"><i style={{width:"62%"}}/></div><div className="muted" style={{marginTop:8}}>Illustrative diligence progress only — not an investment readiness certification.</div></>}
          </div>
          <div className="panel section"><h2>Evidence registry</h2><div className="muted">Public-safe status view</div><table className="table"><thead><tr><th>Batch</th><th>Status</th></tr></thead><tbody>{batches.map(b=><tr key={b.id}><td><strong>{b.id}</strong><div className="muted">{b.site}</div></td><td><span className={b.status==="VERIFIED"?"badge verified":"badge pending-b"}>{b.status}</span></td></tr>)}</tbody></table><button className="secondary" style={{marginTop:14,width:"100%"}} onClick={()=>setActive("Evidence & DMRV")}>Inspect evidence chain</button></div>
        </section>
        <footer className="footer">Blue-Ether OS · M-1 · P1–P17 · S4 evidence gated. This interface is designed to expose evidence status, not manufacture it. Optional climate/carbon/map adapters are integration boundaries and require their own credentials, licensing and validation.</footer>
      </main>
    </div>
  </div>
}
