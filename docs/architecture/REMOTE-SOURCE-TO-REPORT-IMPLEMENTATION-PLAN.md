# Remote Source → Report Implementation Plan

## Outcome

Enable OMI-OJO to assemble reportable project data from approved remote sources and location-scoped project contracts, then expose the same governed values to the frontend and institutional reports.

## Phase 1 — Source normalization

Existing source registry entries become executable adapter contracts. Each adapter returns a canonical observation envelope rather than UI-specific data.

Canonical envelope:

```text
observation_id
project_id
site_id
source_id
provider
variable
value
unit
observed_at
retrieved_at
latitude
longitude
spatial_match
source_class
evidence_class
quality_state
methodology_id
adapter_version
raw_payload_hash
```

## Phase 2 — Location resolver

For each project/site, resolve remote observations against:

- exact coordinates where authorized;
- approved radius/tolerance;
- administrative boundary;
- polygon/geofence where appropriate;
- generalized public location when privacy controls apply.

Store the matching method and result. Never infer project attribution only from a city name when a site-level contract exists.

## Phase 3 — Time resolver

Normalize all timestamps to UTC internally while preserving project-local timezone for reporting. Validate observation time against reporting windows and indicator-specific temporal requirements.

## Phase 4 — Indicator resolver

Map canonical variables to project indicators through the indicator registry. The mapping includes unit conversion, aggregation method, frequency and methodology.

## Phase 5 — Quality and reconciliation

Apply source-specific QC, completeness, range and freshness checks. Where multiple sources exist, create a reconciliation record instead of overwriting one source with another.

## Phase 6 — Reportability engine

Evaluate the project reporting contract and return:

```text
REPORTABLE
CONTEXTUAL_ONLY
PENDING
QUARANTINED
OUT_OF_BOUNDARY
STALE
SOURCE_UNAPPROVED
```

## Phase 7 — Reporting read model

Materialize a project-period reporting snapshot. The frontend, report generator and VDR read from this model.

## Phase 8 — Evidence and dMRV

Where an indicator is subject to dMRV, link the observation set to calculation, evidence package, review and verification records. Remote contextual data may support reconciliation but cannot satisfy a physical-measurement requirement unless the methodology explicitly permits it.

## Phase 9 — Network integrity

Hash the released reporting snapshot and optionally anchor the deterministic root through the configured network adapter. The anchor proves snapshot integrity, not environmental truth.

## Phase 10 — Scheduled refresh

A scheduler refreshes sources according to indicator/source frequency and records successful, stale and failed adapter executions. A failed refresh must preserve the last known observation with its original timestamp rather than presenting it as current.

## Frontend contract

Frontend pages consume:

- `/projects/:id/overview`
- `/projects/:id/data`
- `/projects/:id/evidence`
- `/projects/:id/reports`
- `/projects/:id/dmrv`
- `/projects/:id/claims`

These are logical read-model interfaces; exact API implementation may vary.

## Report generation contract

A report generator receives only a reporting snapshot and template configuration. It cannot reach directly into external providers during rendering. This guarantees reproducibility.

## Operational objective

After implementation, onboarding a new project should primarily require configuration of its geography, sources, methodologies, indicators, evidence requirements and report templates. The core ingestion/dMRV/reporting engines are reused.
