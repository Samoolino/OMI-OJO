# Blue-Ether OS — Investment-Grade Frontend Benchmark

## Purpose

Define the frontend target for the Blue-Ether rainwater + dMRV + ESG/GHG + investment-readiness DApp. This is a product/UI benchmark, not a claim that any referenced external provider is integrated.

## Reference patterns reviewed

- InterWork Alliance Token Taxonomy Framework: platform-neutral taxonomy, machine-readable artifacts, reusable templates, control messages and visualizable classifications. The frontend should expose standards mappings as explainable evidence rather than hide them in code.
- Climate/dMRV platforms: emphasize traceable project → asset → measurement → methodology → verification relationships.
- Institutional climate-finance interfaces: emphasize provenance, methodology, data quality, review status, audit trail, reporting exports, permissions and investment decision context.
- Web3 application patterns: wallet identity, chain status, transaction/proof state and role-aware actions should be visible without allowing speculative UI states to masquerade as verified evidence.

## Frontend scorecard

### 10/10 target dimensions

1. **Evidence integrity** — every metric shows source/status/timestamp.
2. **Investor clarity** — executive summary first, drill-down available.
3. **DMRV depth** — measurement → reporting → verification lineage.
4. **Physical-to-digital continuity** — catchment, rainfall, water, batch, bottle and seal relationships.
5. **ESG/GHG readiness** — methodology, scope, factors, uncertainty and review state.
6. **Institutional controls** — roles, approvals, audit trail and evidence locks.
7. **Interactive spatial UX** — WebGL catchment/project visualization without inventing geospatial data.
8. **Blockchain proof UX** — chain/proof status separated from evidence content.
9. **Investment room** — readiness scorecards, diligence requests, evidence index and export surfaces.
10. **Operational resilience** — degraded/offline/pending states are first-class UI states.

## Proposed information architecture

- `/` — institutional landing + live evidence posture
- `/dashboard` — project command center
- `/projects` — project/catchment portfolio
- `/projects/[id]` — physical + digital project twin
- `/rainfall` — forecast, measured telemetry and reconciliation
- `/harvests` — harvest events and production planning
- `/batches` — batch provenance and quality
- `/batches/[id]` — complete evidence lineage
- `/bottles/[id]` — QR/seal verification
- `/dmrv` — measurement/reporting/verification workspace
- `/esg` — ESG metrics and reporting status
- `/ghg` — methodology and emissions evidence
- `/impact` — environmental/social/economic indicators
- `/verification` — verifier workbench
- `/investors` — investment readiness room
- `/investors/data-room` — controlled evidence index
- `/standards` — IWA/ESG/regulatory mappings
- `/governance` — roles, approvals, audit trail
- `/settings` — sources, integrations and environment status

## Core interactive model

The primary dashboard should expose a visual project twin:

`Atmosphere → Catchment → Collection → Water Quality → Batch → Bottle → Evidence → Proof → Investment`

WebGL is an explanatory/operational visualization layer. It must never be the source of truth; source records and evidence packages remain authoritative.

## Institutional design rules

- Never use green/verified styling for pending evidence.
- Every KPI has a status badge: MEASURED, FORECAST, CALCULATED, MODELLED, ESTIMATED, PROXY, VERIFIED or PENDING.
- Every material claim exposes provenance and methodology.
- Investment readiness is a scored evidence posture, not a promise of financing.
- No simulated number is presented as a live metric.
- Wallet/network state is explicit and role-aware.
- Audit actions require appropriate permissions.
- Confidential evidence is separated from public verification data.

## Reusable frontend primitives

`EvidenceStatus`, `SourceBadge`, `MetricCard`, `EvidenceTimeline`, `MethodologyCard`, `DataQualityMeter`, `ReadinessRing`, `ProjectTwin`, `RainfallChart`, `ReconciliationCard`, `CatchmentMap`, `BatchLineage`, `BottleProof`, `AuditTrail`, `VerificationDecision`, `InvestorDiligenceChecklist`, `StandardsMapping`, `ChainProof`, `ExportPanel`, `RoleGate`, `CommandPalette`.

## Delivery rule

The first frontend increment should be a fully navigable, responsive, accessible shell with deterministic demo data explicitly marked SIMULATED. Subsequent adapters can replace each demo source with repository-backed APIs without redesigning the investor experience.
