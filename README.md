# Blue-Ether OS

**Repository:** `Samoolino/OMI-OJO`  
**System:** Blue-Ether / OMI-OJO Climate-Water Intelligence & Environmental Evidence OS  
**Milestone:** M-1 — Investor-Ready Evidence Core  
**Current state:** Institutional production framework active; controlled runtime and physical validation remain gated.

## UB-02 product position

OMI-OJO is being upgraded as **Climate & Environmental Data + Evidence Infrastructure**. Existing projects and product identifiers are retained; UB-02 adds a common platform architecture across them.

```text
Physical / Edge
  -> Source & Data
  -> Governed Data
  -> dMRV / Evidence
  -> Climate & ESG Intelligence
  -> Institutional Reporting
  -> Network / Integrity
  -> Climate Finance
```

Canonical lifecycle: `REGISTER -> OBSERVE -> MEASURE -> QUALIFY -> CALCULATE -> EVIDENCE -> REVIEW -> RELEASE`.

See `docs/architecture/` and `config/omi-ojo-product-architecture.json`.

## Business definition

OMI-OJO is a **climate-water intelligence and digital MRV infrastructure platform** connecting environmental data, technical measurements, physical water assets, evidence packaging, independent review, ESG/GHG reporting and blockchain integrity anchoring.

**Reference deployment:** Lagos, Nigeria.  
**Expansion thesis:** Europe + Caucasus + Central Asia.  
**Business rule:** `ACTIVITY DATA ≠ ENVIRONMENTAL CLAIM ≠ VERIFIED CARBON CREDIT`.

## Production architecture

```text
M-1 — INVESTOR-READY EVIDENCE CORE
│
├── P1–P20  Software/data/evidence foundation
├── S4      Controlled evidence integration
│   ├── Providers + measured telemetry
│   ├── Rain events + reconciliation
│   ├── Video evidence
│   ├── Water/QMS evidence
│   └── DMRV / ESG / security / regulatory review
├── S5      Global Lagos → EuroAsia expansion architecture
├── S6A     Blockchain + network/builder/grant infrastructure
├── S6B     Builder/grant work-package programme
└── S6C     Lagos physical field validation / Premium RainWater evidence
```

## Institutional evidence chain

```text
Authorization
 → Source / Site Registration
 → Observation / Operation
 → Technical Measurement
 → Quality Control
 → Reconciliation
 → Validation
 → Evidence Package
 → Independent Review
 → DMRV Status
 → Blockchain Integrity Anchor
 → Institutional Report
 → Milestone Acceptance
 → Release / Scale
```

## Product families

1. **OMI-OJO Data** — source, ingestion and governed environmental data.
2. **OMI-OJO Evidence** — dMRV, provenance, reconciliation, review and verification.
3. **OMI-OJO Intelligence** — climate, water, ESG, GHG and climate-risk intelligence.
4. **OMI-OJO Institutional** — funder, investor/VDR, regulatory and audit delivery.
5. **OMI-OJO Edge** — hardware-agnostic physical measurement and field infrastructure.
6. **OMI-OJO Premium** — enhanced physical evidence and methodology-controlled product release.

Legacy product names remain valid implementation labels: OS, Nodes, Intelligence, MRV, Institutional and Premium.

## Climate & ESG Data Framework

| Layer | Function |
|---|---|
| L0 | Physical world / field / edge |
| L1 | Raw and source data |
| L2 | Observations and measurements |
| L3 | Governed data / QC / reconciliation |
| L4 | Environmental intelligence |
| L5 | ESG / GHG / climate risk |
| L6 | dMRV / assurance / verification |
| L7 | Institutional reporting / finance |

## Project continuity

UB-02 preserves `P1–P20`, `S4`, `S5`, `S6A`, `S6B`, `S6C`, the Global Lagos deployment, the Lagos-to-Dubai programme and the Illovediza-Fuerza evidence sequence. The canonical mapping is in `config/omi-ojo-project-registry.json` and `docs/architecture/PROJECT-MAPPING.md`.

## dMRV position

dMRV is a first-class **Evidence Processing Engine**, not merely a frontend page:

`DATA -> NORMALIZE -> QUALITY -> RECONCILE -> CALCULATE -> CLASSIFY -> PACKAGE -> REVIEW -> VERIFY -> ANCHOR -> REPORT`.

The existing `src/dapps/dmrv-portal` remains an implementation seed and is being surfaced through the frontend upgrade as the dMRV Control Centre.

## Investment architecture

The current institutional scope separates the company into four business planes:

- Data & Intelligence
- Measurement & Infrastructure
- Verification & Reporting
- Premium Environmental-Market Evidence

The business case is the evidence infrastructure; environmental-credit activity is a downstream, methodology-dependent application.

See:

- `docs/architecture/UB-02-CLIMATE-ESG-DATA-ARCHITECTURE.md`
- `docs/architecture/PRODUCT-MAP.md`
- `docs/architecture/PROJECT-MAPPING.md`
- `docs/architecture/DMRV-ARCHITECTURE.md`
- `docs/architecture/SOURCE-AND-METHODOLOGY-REGISTRY.md`
- `docs/architecture/GRANTS-NETWORK-BLOCKCHAIN-STRATEGY.md`
- `docs/architecture/REPORT-ARCHITECTURE.md`
- `docs/architecture/FRONTEND-UPGRADE-BLUEPRINT.md`

## Evidence boundary

Forecasts remain forecasts. Measured telemetry remains measured telemetry. Modelled, calculated, estimated and proxy indicators are explicitly labelled. The blockchain layer anchors evidence hashes; raw telemetry is not placed on-chain.

The **400 L/pod/month** value remains a financial-model assumption, not a certified production guarantee. `WAT-002B` and observed pod telemetry govern recalibration before production capacity is treated as bankable.

## Carbon/environmental-credit boundary

OMI-OJO can produce carbon-relevant activity data and support eligible environmental-credit projects, but it does not treat collection activity as an automatic carbon credit. Any credit pathway requires an applicable methodology, baseline, additionality, monitoring plan, calculation, validation, verification and registry issuance/retirement where applicable.

**Current carbon status:** conceptual / carbon-relevant data only.

See `docs/investment/OMI-OJO-CARBON-EVIDENCE-POLICY.md`.

## Funding and network boundary

Builder/testnet/network gas credits are infrastructure resources needed to validate the evidence-anchoring system. Grant requests map funds to measurable work packages and acceptance evidence.

A project token is **DEFERRED** and is not required for the current institutional validation stage. Any future token requires separate legal, tax, accounting, governance and product review.

## Readiness policy

`make readiness` is fail-closed. Empirical rainfall validation, forecast accuracy, controlled provider integration, QMS/water-quality review, DMRV review, GHG methodology review, regulatory review, security review, authorized site surveys and physical field validation remain required before relevant production claims can be released.

The root `Makefile` remains the final operational command surface. Run `make production-check` before any release or deployment.
