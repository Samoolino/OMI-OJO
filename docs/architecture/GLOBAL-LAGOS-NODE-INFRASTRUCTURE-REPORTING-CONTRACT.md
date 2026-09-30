# Global Lagos — Node Infrastructure & Reporting Contract

## Purpose

The 40-node Global Lagos surface is a reporting/read-model layer. It is not an authorization shortcut and it does not convert public web references into physical evidence.

Each node resolves through four independent layers:

1. **Jurisdiction** — LCDA or controlled state/environmental reference.
2. **Public reference** — landmark/address, public imagery or map context.
3. **Infrastructure definition** — what a future authorized deployment would need.
4. **Reporting profile** — which report families, indicators and minimum evidence classes can be considered.

## Infrastructure classes

### LCDA civic node

Default infrastructure definition:
- site-owner authorization
- rain gauge / telemetry mounting assessment
- secure evidence capture point
- power and communications assessment
- maintenance and incident records

Typical contextual indicators:
- rainfall
- temperature
- humidity
- wind
- solar

Evidence promotion requires authorized GIS, source provenance, location/time matching and QC.

### State institutional node

Default infrastructure definition:
- formal institutional authorization
- security/access review
- controlled evidence capture
- power and communications assessment
- custody and audit trail

Residential/security-sensitive locations remain generalized until an authorized precision level is explicitly approved.

### Environmental reference node

Default infrastructure definition:
- authorized environmental reference site
- stewardship/access controls
- future field-evidence boundary
- biodiversity/ecosystem evidence only when actually measured or otherwise supported by an approved method

Public imagery is contextual evidence only.

## Reporting contract

The frontend consumes node reporting profiles from apps/web/app/global-lagos/reporting.ts. Profiles map each node to report families, indicators, minimum evidence requirements and a release rule.

The canonical backend remains authoritative for reportability. Frontend profiles are descriptive read-model metadata and must not independently promote observations to REPORTABLE or VERIFIED.

## Visual-source contract

Each node may expose:
- public image search
- public map candidate
- generalized site view

These surfaces are explicitly labelled **visual reference**. They cannot satisfy:
- site authorization
- measured telemetry
- water-quality verification
- GHG activity-data verification
- DMRV approval
- blockchain truth claims

## Coordinate promotion

PENDING_AUTHORIZED_GIS → CANDIDATE_PUBLIC_REFERENCE → AUTHORIZED is not a valid automatic transition. The authoritative transition requires a recorded authorized GIS/survey source, precision, capture time/version and site authorization. Public candidate coordinates remain non-authoritative.

## Operational next step

jurisdiction → public reference → candidate coordinate → authorized GIS → infrastructure readiness → source adapter → QC → reconciliation → reporting snapshot → DMRV review → release

No later stage may be inferred from an earlier contextual stage.
