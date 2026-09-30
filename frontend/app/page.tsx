'use client';
import { useRef } from 'react';
import * as THREE from 'three';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Float, Environment } from '@react-three/drei';
import { Activity, ArrowUpRight, BarChart3, Boxes, Database, Droplets, FileCheck2, Gauge, Globe2, Layers3, LockKeyhole, Network, ShieldCheck, SlidersHorizontal, Sparkles, Waves } from 'lucide-react';

const nav=[
  ['Overview',Gauge],['Data Observatory',Database],['Evidence & dMRV',FileCheck2],['Climate Intelligence',Sparkles],
  ['ESG / GHG',BarChart3],['Projects',Globe2],['Edge & Field',Droplets],['Institutional',LockKeyhole]
] as const;

const products=[
  ['Data','Sources, telemetry, GIS and governed environmental datasets','L1–L3'],
  ['Evidence','dMRV, provenance, reconciliation, review and integrity','L2–L7'],
  ['Intelligence','Climate, water, ESG, GHG and risk interpretation','L4–L5'],
  ['Institutional','Grant, VDR, audit, disclosure and reporting outputs','L6–L7'],
  ['Edge','Physical nodes, field operations and measurement capture','L0–L2']
];

const projects=[
  ['M-1','Platform baseline','Data · Evidence · Intelligence · Institutional','L0–L7'],
  ['P1–P20','Core capability programme','Core platform capabilities','Capability mapping'],
  ['S4','Controlled evidence integration','Data · Evidence','L1 · L2 · L3 · L6'],
  ['S5','Global deployment framework','Data · Intelligence · Institutional','L1–L7'],
  ['S6A','Network & integrity infrastructure','Evidence · Institutional','L6 · L7'],
  ['S6B','Builder & grant infrastructure','All product layers','L1–L7'],
  ['S6C','Lagos physical validation reference','Edge · Data · Evidence · Water','L0–L7'],
  ['ES4 / ES5 / ES6','Reconciliation + dMRV sequences','Data · Evidence · Institutional','L1–L7']
];

const dmrv=[
  ['1','Source intake','SOURCE','Provider, retrieval time, geography, methodology'],
  ['2','Normalize','NORMALIZED','Canonical unit, schema and temporal boundary'],
  ['3','Quality','QC','Completeness, anomaly and quality state'],
  ['4','Reconcile','RECONCILED','Cross-source comparison and conflict handling'],
  ['5','Calculate','INDICATOR','Methodology + factors + assumptions + uncertainty'],
  ['6','Evidence','PACKAGE','Deterministic evidence package + claim lineage'],
  ['7','Review','REVIEW','Technical / independent review gate'],
  ['8','Anchor','INTEGRITY','Optional network/blockchain anchor'],
  ['9','Release','REPORT','Controlled public, grant, ESG, GHG, VDR or audit output']
];

const evidence=[['Rainfall forecast','FORECAST','Source + retrieval timestamp'],['Site telemetry','MEASURED','Awaiting validated field dataset'],['Water quality','PENDING','Lab/QMS evidence required'],['Evidence root','CALCULATED','Deterministic SHA-256 package'],['Blockchain proof','DRY-RUN','Integrity adapter only']];

function ProjectTwin(){const mesh=useRef<THREE.Mesh>(null);useFrame((_,d)=>{if(mesh.current)mesh.current.rotation.y+=d*.12});return <Canvas camera={{position:[0,1.2,5],fov:48}}><ambientLight intensity={1.3}/><directionalLight position={[3,4,2]} intensity={3}/><Environment preset="night"/><Float speed={1.3} rotationIntensity={.25} floatIntensity={.45}><mesh ref={mesh}><icosahedronGeometry args={[1.45,3]}/><meshStandardMaterial color="#1b6b57" metalness={.35} roughness={.25} wireframe/></mesh></Float><mesh position={[0,-1.75,0]} rotation={[-Math.PI/2,0,0]}><circleGeometry args={[2.8,64]}/><meshStandardMaterial color="#0d211c" metalness={.1} roughness={.8}/></mesh><OrbitControls enablePan={false} minDistance={3} maxDistance={7}/></Canvas>}
function Metric({label,value,detail}:{label:string,value:string,detail:string}){return <div className="card metric"><div className="label">{label}</div><div className="value">{value}</div><div className="delta">{detail}</div></div>}
function Status({children,pending=false}:{children:string,pending?:boolean}){return <span className={'badge '+(pending?'pending':'')}>{children}</span>}

export default function Home(){return <div className="app"><header className="topbar"><div className="brand"><div className="mark"><Droplets size={18}/></div><div><strong>OMI-OJO</strong><small>CLIMATE & ENVIRONMENTAL DATA + EVIDENCE INFRASTRUCTURE</small></div></div><div className="status"><span className="dot"/> UB-02 · DATA → EVIDENCE → INTELLIGENCE → INSTITUTIONAL</div></header><div className="layout"><aside className="nav"><div className="section">Platform</div>{nav.slice(0,4).map(([name,Icon],i)=><a className={i===0?'active':''} href="#" key={name}><Icon size={15}/>{name}</a>)}<div className="section">Institutional</div>{nav.slice(4).map(([name,Icon])=><a href="#" key={name}><Icon size={15}/>{name}</a>)}<div className="section">Control</div><a href="#dmrv"><SlidersHorizontal size={15}/>dMRV Control Centre</a><a href="#projects"><Network size={15}/>Project Registry</a><a href="#methods"><Layers3 size={15}/>Sources & Methods</a><a href="#audit"><Activity size={15}/>Audit Trail</a></aside><main className="main">
<section className="hero"><div><div className="eyebrow">Climate & ESG data control plane</div><h1>From physical observation to institutional-grade environmental evidence.</h1><p>OMI-OJO connects verified data sources, field measurements, dMRV, methodology lineage, ESG/GHG intelligence and network integrity without treating blockchain as a source of environmental truth.</p></div><div className="actions"><button className="button">Open evidence index</button><button className="button primary">Open institutional room <ArrowUpRight size={13}/></button></div></section>
<section className="grid4"><Metric label="Architecture" value="L0–L7" detail="Physical → data → evidence → institutional"/><Metric label="Product families" value="5" detail="Data · Evidence · Intelligence · Institutional · Edge"/><Metric label="Project registry" value="M-1 + P1–P20 + S4–S6C" detail="Historical identifiers retained"/><Metric label="Release posture" value="Fail-closed" detail="No unsupported production claims"/></section>
<section className="grid2"><div className="card viz"><ProjectTwin/><div className="overlay"><div className="eyebrow">Interactive system twin</div><div className="title">Physical → data → evidence → intelligence topology</div></div><div className="legend"><span><i/>physical</span><span><i/>data</span><span><i/>evidence</span><span><i/>institutional</span></div></div><div className="card"><div className="eyebrow">Product architecture</div><h3 style={{margin:'8px 0 0',fontFamily:'Manrope'}}>One platform, reusable project adapters</h3><div className="list">{products.map(([a,b,c])=><div className="row" key={a}><div><strong>OMI-OJO {a}</strong><small>{b}</small></div><Status>{c}</Status></div>)}</div></div></section>
<section id="dmrv" className="card"><div className="eyebrow">First-class evidence processing engine</div><h3 style={{fontFamily:'Manrope'}}>dMRV Control Centre</h3><p className="muted">dMRV is the processing and assurance layer between governed data and institutional outputs. The frontend exposes the workflow; canonical evidence remains the source of release decisions.</p><div className="list">{dmrv.map(([n,a,b,c],i)=><div className="row" key={n}><div><strong>{n}. {a}</strong><small>{c}</small></div><Status pending={i===1||i===2||i===6}>{b}</Status></div>)}</div></section>
<section className="grid2"><div className="card"><div className="eyebrow">Evidence posture</div><h3 style={{fontFamily:'Manrope'}}>Current evidence pipeline</h3><div className="list">{evidence.map(([a,b,c],i)=><div className="row" key={a}><div><strong>{a}</strong><small>{c}</small></div><Status pending={i===1||i===2}>{b}</Status></div>)}</div></div><div id="methods" className="card"><div className="eyebrow">Governed data</div><h3 style={{fontFamily:'Manrope'}}>Source + Methodology registries</h3><div className="row"><div><strong>Source Registry</strong><small>Provider, geography, resolution, provenance, validation state and version.</small></div><Status>CANONICAL</Status></div><div className="row"><div><strong>Methodology Registry</strong><small>Formula, assumptions, uncertainty, evidence requirements, permitted claims and supersession.</small></div><Status>CANONICAL</Status></div><div className="row"><div><strong>Claims Registry</strong><small>Claim → evidence → methodology → audience → review/expiry.</small></div><Status>CONTROLLED</Status></div></div></section>
<section id="projects" className="card"><div className="eyebrow">Programme continuity</div><h3 style={{fontFamily:'Manrope'}}>Project Registry · retained IDs, upgraded mappings</h3><div className="list">{projects.map(([id,role,product,layers])=><div className="row" key={id}><div><strong>{id}</strong><small>{role} · {product}</small></div><Status>{layers}</Status></div>)}</div></section>
<section className="grid2"><div className="card"><div className="eyebrow">Physical → digital lineage</div><h3 style={{fontFamily:'Manrope'}}>Controlled evidence lifecycle</h3><div className="timeline"><div className="event"><b>Register</b><p>Project, site, asset, node, source and methodology boundaries are established.</p></div><div className="event"><b>Observe → Measure</b><p>Forecast/modelled values remain labelled until measured evidence reconciles them.</p></div><div className="event"><b>Qualify → Calculate</b><p>QC, reconciliation, calculation factors, assumptions and uncertainty remain traceable.</p></div><div className="event"><b>Evidence → Review → Release</b><p>Claims are packaged, reviewed, optionally anchored and rendered into controlled reports.</p></div></div></div><div id="audit" className="card"><div className="eyebrow">Network + grants</div><h3 style={{fontFamily:'Manrope'}}>Infrastructure, not environmental truth</h3><div className="row"><div><strong>Grant work package</strong><small>Grant → capability → milestone → evidence → acceptance.</small></div><Status>STRUCTURED</Status></div><div className="row"><div><strong>Network anchor</strong><small>Deterministic evidence root → adapter → transaction → verification.</small></div><Status>DRY-RUN</Status></div><div className="row"><div><strong>Public verifier</strong><small>Evidence ID → package root → anchor proof → verification result.</small></div><Status>PLANNED</Status></div><div className="row"><div><strong>Token</strong><small>Explicitly deferred; not a prerequisite for evidence infrastructure.</small></div><Status pending>DEFERRED</Status></div></div></section>
<div className="footer"><span>OMI-OJO · Evidence before assertion</span><span>Architecture UI · production gates remain authoritative</span></div></main></div></div>}
