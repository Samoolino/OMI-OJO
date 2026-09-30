# OMI-OJO dMRV Architecture

## Position

dMRV is a **platform engine**, not a dashboard page. It sits between governed data and institutional outputs.

```text
DATA -> NORMALIZE -> QUALITY -> RECONCILE -> CALCULATE -> CLASSIFY -> PACKAGE -> REVIEW -> VERIFY -> ANCHOR -> REPORT
```

## Canonical dMRV objects

1. Observation
2. Normalized observation
3. Quality assessment
4. Reconciliation result
5. Indicator
6. Calculation
7. Evidence item
8. Evidence package
9. Claim
10. Review decision
11. Verification result
12. Anchor record
13. Report/VDR artifact

## Frontend control centre

The frontend should expose these queues/views:

- Evidence Inbox
- Data Quality
- Reconciliation
- Indicator & Calculation Lineage
- Evidence Graph
- Package Builder
- Review Queue
- Verification
- Anchor Registry
- Release Gate

The existing `src/dapps/dmrv-portal` remains the implementation seed; it is not replaced.

## Evidence lineage

```text
Claim
  -> Evidence
    -> Observation / Measurement
      -> Source
      -> Methodology
      -> Calculation
      -> QC / Reconciliation
      -> Reviewer
      -> Verification
      -> Integrity anchor
```

## Claim controls

Every material claim must identify:

- claim id
- statement
- evidence ids
- source ids
- methodology/version
- geography and reporting period
- review state
- permitted audience
- limitations
- expiry/review date

## GHG alignment

GHG results require explicit activity data, factor source/version, calculation method/version, assumptions and uncertainty. The calculation lineage must be preserved in the evidence package.

## dMRV and ESG

ESG is a downstream governed interpretation layer. Environmental observations are not automatically ESG-compliant disclosures. The dMRV engine supplies the provenance and assurance context required for controlled ESG reporting.

## dMRV and blockchain

Only the deterministic evidence package/root is anchored. Anchoring does not upgrade evidence class or establish environmental truth.

## Release states

`DRAFT -> QC_READY -> REPORTABLE -> REVIEWED -> VERIFIED -> ANCHORED -> RELEASED`

A failed or incomplete control moves to `HOLD`, not silently to the next state.
