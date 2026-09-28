# OMI-OJO UB-02 — Climate & ESG Data Architecture

## Purpose

UB-02 upgrades OMI-OJO from a set of project/product surfaces into a reusable Climate & Environmental Data and Evidence infrastructure platform. Existing projects, production gates, evidence contracts and historical identifiers are retained.

## Canonical platform spine

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

Cross-cutting controls: governance, authorization, security, privacy, methodology, claims, regulatory scope and release gates.

## Canonical lifecycle

`REGISTER -> OBSERVE -> MEASURE -> QUALIFY -> CALCULATE -> EVIDENCE -> REVIEW -> RELEASE`

## Canonical entities

`Organization -> Project -> Site -> Asset -> Node -> Observation -> Measurement -> Calculation -> Evidence -> Claim -> Review -> Verification -> Report`

## Climate & ESG mapping

| Layer | Function | OMI-OJO capability |
|---|---|---|
| L0 | Physical world | Edge, field, sensors, QMS |
| L1 | Raw/source data | Source Registry, APIs, documents, telemetry |
| L2 | Observations/measurements | Immutable observation schemas, field records |
| L3 | Governed data | normalization, QC, reconciliation, provenance |
| L4 | Environmental intelligence | climate, water, air, energy, land, biodiversity |
| L5 | ESG/GHG/risk | E/S/G metrics, activity data, calculations, risk |
| L6 | dMRV/assurance | evidence graph, review, verification, release gates |
| L7 | institutional/finance | reports, VDR, grants, audit, investment, climate finance |

## Product families

1. **OMI-OJO Data** — environmental data infrastructure.
2. **OMI-OJO Evidence** — dMRV, provenance, reconciliation, review and verification.
3. **OMI-OJO Intelligence** — climate, water, ESG, GHG and climate-risk intelligence.
4. **OMI-OJO Institutional** — VDR, grant, investor, regulator and audit delivery.
5. **OMI-OJO Edge** — physical nodes, sensors, telemetry and field operations.
6. **OMI-OJO Premium** — advanced physical evidence and methodology-controlled product release.

Legacy product names remain valid as implementation labels: OS, Nodes, Intelligence, MRV, Institutional and Premium.

## Non-negotiable architecture rules

- Existing P1–P20, S4, S5, S6A, S6B and S6C identifiers are retained.
- No project is deleted or renamed solely for architectural consistency.
- Project-specific adapters configure the common platform; bespoke pipelines require justification.
- Data class is never upgraded by presentation alone.
- Blockchain establishes integrity of a deterministic evidence root; it does not establish environmental truth, regulatory compliance, water quality or funding.
- Activity data is not itself a verified carbon credit.
- International deployments inherit evidence semantics, not unsupported values from another geography.
- Funding status is separate from technical readiness.
- Project token remains deferred unless a separately approved policy changes that state.
- Physical production remains gated by the production manifest.

## Release vocabulary

`DESIGNED | IMPLEMENTED | INTEGRATION_READY | CONTROLLED_TEST | REPORTABLE | VALIDATED | VERIFIED | ANCHORED | RELEASED | HOLD | DEFERRED`

## Evidence classes

`OBSERVED | FORECAST | MODELLED | SATELLITE | CALCULATED | PROXY`

## Implementation sequence

1. Architecture and registries.
2. Canonical project adapters.
3. dMRV control surface.
4. Frontend information architecture.
5. ESG/GHG/reporting engines.
6. Grant/network/blockchain integration.
7. Production validation and controlled release.
