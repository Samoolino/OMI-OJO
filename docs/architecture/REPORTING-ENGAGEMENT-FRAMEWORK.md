# OMI-OJO Reporting Engagement Framework

## Objective

Make every OMI-OJO project reportable through a common technical reporting contract while allowing each engagement to define its own geography, indicators, methodologies, evidence thresholds and report outputs.

## Engagement model

Every engagement is represented as:

`ENGAGEMENT → PROJECT(S) → SITE(S) → DATA CONTRACT → SOURCE SET → METHODOLOGY SET → INDICATORS → EVIDENCE POLICY → REPORT SET → RELEASE GATES`

## Required engagement fields

- engagement_id
- project_ids
- client/institutional audience
- geography and sites
- reporting period
- reporting frequency
- indicators
- source allowlist
- methodology allowlist
- minimum evidence class
- reconciliation policy
- report templates
- publication audience
- retention policy
- release gate

## Standard report families

### 1. Project status report

Project progress, data coverage, evidence state, gates, risks and exceptions.

### 2. Environmental data report

Canonical observations and indicators with source, location, period, quality and freshness.

### 3. Climate report

Climate variables, hazards, anomalies, trends and contextual model outputs.

### 4. Water report

Rainfall, collection, storage, quality, use, resilience and physical validation evidence where applicable.

### 5. ESG report

Environmental, social and governance metrics mapped to underlying evidence and applicable disclosure methodology.

### 6. GHG report

Scope/boundary, activity data, factors, formulas, assumptions, uncertainty, result and evidence lineage.

### 7. dMRV/evidence report

Observation lineage, QC, reconciliation, evidence packages, reviews and verification state.

### 8. Grant/funder report

Work package, milestone, expenditure/inputs where authorized, outputs, evidence, acceptance and next gate.

### 9. Investor/VDR report

Technical, environmental, evidence, commercial, security and deployment diligence.

### 10. Regulatory/audit report

Jurisdiction-specific required fields plus complete provenance and review history.

## Single-source reporting principle

Reports are generated from the canonical reporting read model. Individual report templates do not maintain separate copies of environmental data.

## Reporting snapshot

Before release, the system creates a versioned snapshot containing:

- reporting period
- project/site scope
- source versions
- observation IDs
- indicator IDs
- calculation IDs
- methodology versions
- evidence package IDs
- reviewer decisions
- release gate state

The snapshot receives a deterministic hash. Where configured, the hash may be anchored through the OMI-OJO network layer.

## Frontend reporting workflow

`Select Project → Select Reporting Period → Review Data Coverage → Review Exceptions → Inspect Evidence → Generate Draft → Review → Approve → Release → Verify`

The UI must clearly distinguish:

- Draft
- Internally reviewed
- Reportable
- Published
- Superseded

## Engagement isolation

A source may be reused across engagements, but a report never inherits another project's values. The project adapter resolves geography, time, indicator and methodology independently.

## Remote reporting objective

Once source adapters and project contracts are configured, each active project can continuously assemble a reportable data view from approved remote sources. This is a platform capability, not a claim that every current project already has complete live source coverage.

## Exceptions

Missing remote data, provider outages, location ambiguity, stale data, methodology gaps and physical-validation requirements produce explicit exceptions. They do not become blank values or silent substitutions.

## Institutional delivery

The same reporting snapshot can feed the public portal, grant report, ESG/GHG report, VDR, audit package and regulator-specific report, with audience-specific redaction and evidence thresholds.
