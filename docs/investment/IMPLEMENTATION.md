# P19 — Investment Readiness Implementation

## Implemented in this milestone

- Investment VDR room taxonomy.
- Machine-readable VDR schema.
- ESG evidence/reporting covenant.
- SAFE-aligned, counsel-ready term sheet.
- Evidence status lifecycle.
- Explicit modeled-vs-measured rainfall boundary.

## Runtime integration target

The application should progressively map the VDR schema to the DMRV evidence registry and investor portal. Evidence objects should be addressable by event/activity ID and expose provenance, methodology, hash and verification state.

## Investment readiness state

`DRAFT → EVIDENCE_PENDING → EVIDENCE_CAPTURED → DMRV_VALIDATED → VERIFIER_REVIEW → VERIFIED → INVESTOR_READY`

## Physical rainfall evidence

`CATCHMENT → FIRST_FLUSH → COLLECTOR → EVENT → SAMPLE → HASH → LAB/QA → VERIFIED`

The physical collector is the measured evidence boundary. Open-Meteo remains a modeled contextual/reference source.

## SAFE boundary

The repository contains a commercial term-sheet framework only. No executable securities issuance, investor funds movement, token sale, or automatic SAFE execution is implemented by this milestone.

## Next implementation layer

1. VDR metadata API/schema validation.
2. Investor evidence-card UI.
3. Read-only investor portal.
4. Evidence readiness score derived from actual records.
5. ESG report generation from verified evidence.
6. Cap-table/SAFE metadata model after jurisdiction-specific counsel approval.
