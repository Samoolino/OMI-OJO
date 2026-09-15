# OMI-OJO — Institutional Submission Specification

**Purpose:** submission-control sheet for INMerge, institutional investors, grants, climate-finance partners and strategic pilots.

## 1. Claim classes

Every claim in a deck, VDR, application or public page must carry an internal evidence class:

- `ACTUAL` — contractual/financial/business fact supported by source records.
- `OBSERVED` — directly observed/measured field or provider data.
- `FORECAST` — forward-looking provider/model output.
- `MODELLED` — model output with stated assumptions.
- `CALCULATED` — deterministic calculation from referenced evidence.
- `PROXY` — indirect indicator; must not be represented as direct measurement.
- `TARGET` — planned milestone, not achieved performance.

## 2. Proof gates

`P0 CONCEPT → P1 TECHNICAL → P2 FIELD/PRODUCT → P3 INSTITUTIONAL`

No investor-facing material may promote a P0/P1 claim as field or institutional proof.

## 3. ESG reporting object

Minimum reporting record:

`project_id, site_id, node_id, reporting_period, indicator_id, value, unit, evidence_class, source, methodology_version, timestamp, geography, QC_state, reconciliation_state, uncertainty, reviewer_state, release_state, evidence_root`

## 4. Measurement controls

### Rainfall
Source/provider, observation timestamp, location, retrieval method, unit, missing-data rule and observed-vs-forecast classification.

### Water collection
Catchment area, event window, storage state, flow/volume measurement, first-flush state, instrument identity and reconciliation to rainfall/capacity.

### Water quality
Sample ID, custody, laboratory method/results, QMS status and applicable regulatory interpretation.

### Carbon-relevant indicators
Project boundary, baseline/counterfactual, activity, emission factor/source, calculation version, uncertainty, additionality evidence where required and double-counting controls.

## 5. Technical stack acceptance

- Data ingestion: source/provider registry and provenance.
- Telemetry: instrument/node identity and timestamps.
- Intelligence: forecast/observation separation and model assumptions.
- Evidence: canonical schema and deterministic package generation.
- Integrity: SHA-256 evidence root; blockchain anchor optional.
- Reporting: public-safe, ESG/GHG, VDR and verification outputs.
- Governance: review roles, audit lineage, release gates and security controls.

## 6. Premium product acceptance

Premium is commercially complete only when the system can demonstrate:

1. enhanced measurement capture;
2. provenance/QMS linkage;
3. baseline/additionality evidence fields where relevant;
4. calculation lineage;
5. reviewer workflow;
6. methodology-version reference;
7. evidence index suitable for external validation/verification.

Premium must never be described as automatic carbon-credit issuance.

## 7. Investment submission pack

### Core files

1. Pitch deck V3.
2. Executive summary.
3. Business Scope.
4. Business Logic.
5. Verification Architecture.
6. Carbon Evidence Policy.
7. Technical architecture.
8. Product demo URL.
9. VDR index.
10. Capital-to-output milestone plan.

### Supporting evidence

- repository/commit references;
- controlled test results;
- provider/source registry;
- field/site authorization when available;
- calibration/QMS records when available;
- financial records for actual revenue/funding;
- founder/team records;
- IP ownership documentation;
- legal/entity documentation.

## 8. Investor language standard

Use:

> “carbon-relevant activity data”
> “methodology-ready evidence”
> “environmental-credit eligibility pathway”
> “subject to independent validation/verification and registry rules”

Avoid unless independently established:

> “certified credits”
> “verified carbon reduction”
> “guaranteed credits”
> “guaranteed water production”
> “blockchain-verified environmental impact”

## 9. Capital request discipline

Every funding request must map to:

`CAPITAL → WORK PACKAGE → TECHNICAL OUTPUT → ACCEPTANCE EVIDENCE → COMMERCIAL/INSTITUTIONAL GATE`

No funding case should rely solely on projected carbon-credit revenue.
