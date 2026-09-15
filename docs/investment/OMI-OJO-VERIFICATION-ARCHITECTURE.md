# OMI-OJO — Verification Infrastructure & Product Proof Architecture

**Version:** 1.0  
**Milestone:** M-1 — Investor-Ready Evidence Core  
**Purpose:** define the technical/business boundary between environmental activity, measurement, evidence, verification, institutional reporting and future carbon/environmental-credit eligibility.

## 1. Core business rule

OMI-OJO sells an evidence infrastructure product. The product does not sell an environmental claim merely because data exists.

`ACTIVITY → MEASUREMENT → QC → RECONCILIATION → VALIDATION → REVIEW → VERIFICATION → REPORT → INTEGRITY ANCHOR`

Carbon/environmental-credit eligibility is a downstream methodology layer:

`ELIGIBILITY → BASELINE → ADDITIONALITY → MONITORING → CALCULATION → VALIDATION → VERIFICATION → ISSUANCE`

## 2. Technical evidence object

Each material observation or measurement should be represented with, at minimum:

- evidence_id
- project_id
- site_id / node_id
- timestamp
- geographic reference
- variable
- value
- unit
- evidence_class
- source/provider
- instrument or acquisition method
- methodology/version
- quality status
- reconciliation status
- uncertainty/assumption reference
- parent/derived evidence references
- SHA-256 evidence/package root
- reviewer status
- release status

Evidence classes remain explicit:

`OBSERVED | FORECAST | MODELLED | SATELLITE | CALCULATED | PROXY`

## 3. Product proof ladder

### P0 — Concept proof
Architecture, hypothesis, assumptions and intended use are documented.

### P1 — Technical proof
Schemas, APIs, calculations, test fixtures and deterministic package generation operate in controlled tests.

### P2 — Field/product proof
Authorized physical measurements and product operations produce reproducible records.

### P3 — Institutional proof
Required technical review, QMS, ESG/GHG review, independent verification and release controls have passed.

The investor deck must label each claim with the highest evidence layer actually achieved.

## 4. Measurement controls

### Rainfall
Provider/source, timestamp, coordinate, retrieval method, units, missing-data handling and forecast-versus-observation distinction.

### Water collection
Catchment area, event start/end, storage state, flow/volume measurement, first-flush status, instrument identity and reconciliation to rainfall/capacity.

### Water quality
Sampling identity, custody, laboratory method/result, QMS status and applicable regulatory interpretation.

### Environmental indicators
Indicator definition, calculation formula, source factors, version, uncertainty and reviewer status.

## 5. Verification infrastructure

The system should expose separate states:

`DESIGNED → IMPLEMENTED → INTEGRATION_READY → CONTROLLED_TEST → REPORTABLE → VALIDATED → VERIFIED → ANCHORED → RELEASED`

A blockchain anchor records an evidence/package hash and proof of integrity. It does not independently prove physical truth, methodology eligibility or carbon issuance.

## 6. Reporting products

### Public-safe report
Selected non-sensitive metrics, evidence status, provenance and verification state.

### Institutional ESG/GHG report
Methodology, measured activity, calculations, assumptions, evidence references, reviewer status and limitations.

### Investor/VDR package
Business milestones, technical acceptance, deployment evidence, commercial evidence, risk register and capital-to-output mapping.

### Verification package
Deterministic evidence index, source records, calculations, QC/reconciliation, reviewer decisions and integrity proofs.

## 7. Premium product

**OMI-OJO Premium Water Evidence / Carbon Amplification Layer** is an add-on to the core evidence platform.

It may provide:

- higher-frequency measurement and evidence capture;
- enhanced telemetry and sensor integration;
- water-quality/QMS evidence workflows;
- expanded environmental indicator library;
- methodology-ready carbon-relevant data packaging;
- baseline/additionality evidence management;
- independent-review coordination;
- registry/standard evidence preparation where applicable;
- enhanced investor and climate-finance reporting.

**Premium does not manufacture carbon credits.** It amplifies the quality, continuity and usefulness of evidence that may support an eligible methodology. No credit volume, issuance or financial return is promised without the applicable external methodology and verification pathway.

## 8. Commercial packaging

### Core
OS + reporting + evidence registry + standard DMRV workflow.

### Professional
Core + nodes + telemetry + advanced analytics + institutional reporting.

### Premium
Professional + enhanced evidence frequency + QMS/water-quality + methodology/carbon-readiness + verification coordination + climate-finance evidence room.

### Enterprise / Project
Deployment, integrations, custom methodology configuration, VDR, governance and multi-site programme management.

## 9. Investment-grade acceptance

A funded work package is accepted only against predefined evidence. Examples:

| Work package | Output | Acceptance evidence |
|---|---|---|
| Data | provider + telemetry integration | provenance/QC/reconciliation tests |
| Measurement | authorized field node | measured dataset + calibration/measurement record |
| DMRV | evidence package | deterministic package + reviewer workflow |
| Integrity | anchor | reproducible hash/proof test |
| ESG/GHG | methodology pack | calculation + source + review record |
| Premium | enhanced project package | methodology-ready evidence index |
| Field pilot | Lagos deployment | site authorization + field/QMS records |
| Expansion | EuroAsia adapter | country-specific controlled test |

## 10. Carbon claim boundary

`CARBON-RELEVANT DATA ≠ CALCULATED REDUCTION ≠ VERIFIED REDUCTION ≠ ISSUED CREDIT`

Water capture/reuse only becomes carbon-relevant where an eligible methodology can establish the relevant counterfactual, emissions factors, additionality and monitoring requirements. OMI-OJO therefore treats carbon amplification as a premium evidence service, not as automatic credit creation.
