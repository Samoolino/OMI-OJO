# S13 — Institutional First Live Harvest & Evidence Event Execution

## Status
**READY FOR AUTHORIZED FIELD EXECUTION — NO LIVE EVENT CLAIMED**

S13 is the first sequence permitted to create genuine field observations. This document is an execution control, not evidence that a harvest has occurred.

## Mandatory precondition
S12.17 must be human-authorized and its authorization record must be available before event activation.

## Controlled sequence

1. **RAIN-EVENT WATCH** — use approved rainfall/weather sources and preserve provenance. Forecast data remains forecast.
2. **EVENT ACTIVATION** — create a unique event ID and bind it to the authorized physical site, operator, authorization and timestamps.
3. **PRE-EVENT SITE CHECK** — confirm physical site, collector, storage, first-flush, instruments, video, sampling materials and safety controls.
4. **FIRST-FLUSH DIVERSION** — execute and timestamp the approved diversion procedure.
5. **CONTROLLED COLLECTION** — collect only within the authorized boundary; record actual measurements only.
6. **LIVE MEASUREMENT + VIDEO** — synchronize device identity, measurement time, event ID, video identity and operator.
7. **SAMPLE IDENTIFICATION** — create sample IDs only when an actual sample is taken.
8. **CHAIN OF CUSTODY** — record each actual custody transfer and storage condition; material breaks cause HOLD/review.
9. **QMS / LAB HANDOFF** — only an actual sample enters the laboratory pathway; preserve method and version.
10. **BATCH + SEAL** — create traceability identifiers only from an actual controlled production event.
11. **DMRV EVENT PACKAGE** — assemble source observations, field records, measurements, video, custody/QMS, traceability, methods, boundaries, factors, derived metrics and exceptions.
12. **EVIDENCE RECONCILIATION** — reconcile identity, timestamps, units, provenance, measurement lineage, custody/QMS lineage, traceability, methodology and exceptions.
13. **ANCHOR CANDIDATE** — calculate package digest only after reconciliation. An anchor proves package integrity, not environmental truth.
14. **ASSURANCE REVIEW** — apply approved scope and record findings and limitations.
15. **PREMIUM-CONDITION DECISION** — apply predefined evidence criteria; rainfall occurrence alone cannot establish premium status.
16. **REGULATORY / PRODUCT RELEASE GATE** — release remains separate and depends on applicable requirements.

## Event states
PLANNED → ACTIVATED → RAIN_CONFIRMED → COLLECTION_ACTIVE → COLLECTION_COMPLETE → CUSTODY_ACTIVE → QMS_HANDOFF → TRACEABILITY_COMPLETE → DMRV_RECONCILIATION → ANCHOR_CANDIDATE → ASSURANCE_REVIEW → PREMIUM_DECISION → RELEASE_REVIEW

Terminal controls: HOLD, REJECTED, CORRECTIVE_ACTION, REOPENED, SUPERSEDED, RELEASED.

## Fail-closed rules
Any material break in site identity, source provenance, measurement integrity, first-flush evidence, video linkage, custody, QMS lineage, batch reconciliation, methodology, or authorization prevents progression to the next dependent gate.

## Prohibited substitutions
forecast for observation; municipality for physical site; model grid for field measurement; API availability for live evidence; synthetic value for field observation; anchor for verification; DMRV dashboard for environmental truth; readiness for harvest; harvest for product release.

## Current production declaration
No S13 live harvest is asserted by this implementation. The repository is prepared to capture one only when the authorized physical event actually occurs.
