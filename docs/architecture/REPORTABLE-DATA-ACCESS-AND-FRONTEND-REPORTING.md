# OMI-OJO Reportable Data Access & Frontend Reporting Architecture

## Purpose

Define how every project obtains reportable environmental/climate/ESG data from remote sources and project locations, while preserving source class, geographic scope, methodology, evidence state and release gates.

## Core rule

**Availability is not reportability.** A remote observation can be displayed as contextual data before it is eligible for a report. A project report may only consume observations whose source, geography, temporal coverage, methodology and evidence state satisfy that project's reporting contract.

## Canonical pipeline

`PROJECT → LOCATION → DATA REQUIREMENTS → SOURCE REGISTRY → REMOTE ADAPTER → RAW OBSERVATION → NORMALIZATION → LOCATION MATCH → TIME MATCH → QC → RECONCILIATION → INDICATOR → EVIDENCE STATE → REPORTABILITY GATE → REPORT OUTPUT`

## Project location contract

Each project declares:

- project_id
- geography/country
- site_id(s)
- latitude/longitude or approved generalized geometry
- spatial tolerance/radius where applicable
- temporal reporting window
- timezone
- required indicators
- accepted source classes
- required evidence class
- methodology version(s)
- report types
- release gates

Location matching is deterministic and recorded. A source observation outside the configured spatial/temporal boundary is not silently attributed to the project.

## Source classes

- **MEASURED** — authorized physical instrumentation or field measurement.
- **VERIFIED_MEASUREMENT** — measured data that has passed applicable QA/QC or laboratory controls.
- **AUTHORITATIVE_EXTERNAL** — authoritative external institutional source.
- **SATELLITE** — remote-sensing observation.
- **REANALYSIS** — retrospective model/reanalysis product.
- **FORECAST** — forecast/modelled contextual data.
- **COMMERCIAL_API** — provider API subject to source review.
- **PROXY** — explicitly labelled proxy data.

Source class is immutable for the observation. Reconciliation can compare classes but cannot silently promote a lower class into a higher class.

## Remote-source execution model

Adapters support:

- polling APIs
- push streams/webhooks
- archive queries
- file/object ingestion
- satellite/remote-sensing feeds
- manually uploaded controlled evidence

Every ingestion creates an immutable raw record with provider, source_id, retrieval timestamp, observed timestamp, request parameters/query boundary, location, units, raw payload hash and adapter version.

The repository already has an Open-Meteo adapter boundary and Global Lagos provider/indicator registries; these remain contextual/remote-source infrastructure rather than automatic proof of physical measurement.

## Reportability states

`DISCOVERED → INGESTED → NORMALIZED → LOCATION_MATCHED → TIME_MATCHED → QC_PASSED → RECONCILED → REPORTABLE`

Alternative terminal states:

`CONTEXTUAL_ONLY`, `QUARANTINED`, `REJECTED`, `STALE`, `OUT_OF_BOUNDARY`, `SOURCE_UNAPPROVED`.

## Reportable observation contract

An observation is reportable only when:

1. the source is registered;
2. the source is approved for the project and indicator;
3. geography matches the project boundary;
4. time falls inside the project reporting window;
5. unit and variable normalization succeeds;
6. required QC passes;
7. required reconciliation rules pass or an explicit exception is recorded;
8. the methodology version is compatible;
9. the evidence class is permitted by the report type;
10. the release gate allows publication.

## Frontend integration

The frontend should never fetch arbitrary provider APIs directly for report cards. It reads the canonical OMI-OJO reporting API/read model.

### Data Observatory

Shows source observations with:

- source/provider
- location match
- time match
- evidence class
- quality state
- freshness
- methodology
- reconciliation state
- reportability

### Project workspace

Shows only indicators configured for that project, with a toggle for:

- Reportable
- Contextual
- Pending validation
- Quarantined

### Report Builder

A project report is generated from a versioned reporting snapshot, not from live dashboard values. The snapshot contains the observation IDs, calculation IDs, evidence IDs, methodology versions and source versions used.

### Evidence Explorer

Every displayed report value links back through:

`REPORT → INDICATOR → CALCULATION → OBSERVATION(S) → SOURCE → LOCATION/TIME MATCH → EVIDENCE`

## Reporting engagement strategy

All ongoing engagements use one canonical engine and declare their own reporting contract. The same remote source may serve multiple projects, but each project receives an independently evaluated observation set.

Example:

`Open-Meteo rainfall at Lagos` can be contextual evidence for several projects, but it is never copied into another geography merely because the indicator name is the same.

## Data freshness

Each indicator declares a freshness SLA appropriate to its nature. Forecasts, current weather, reanalysis, satellite products and measured field data have different freshness semantics. The report layer records the actual retrieval/observation time rather than implying real-time status.

## Global deployment rule

International projects inherit canonical schemas and evidence semantics, not Lagos observations. Geography, source availability, methodology applicability and local authorization are evaluated independently.

## Security and provenance

Provider credentials remain server-side. The frontend receives normalized records and signed/reporting snapshot identifiers. Sensitive site coordinates can be generalized in public reports while remaining precise inside authorized evidence/VDR views.
