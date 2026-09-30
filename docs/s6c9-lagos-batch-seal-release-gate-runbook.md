# S6C.9 — Lagos Batch and Seal Release Gate Runbook

## Objective
Create a uniquely traceable batch and seal record only after the upstream collection, custody and QMS/analysis evidence required for the intended release decision has been reconciled.

## Scope
S6C.9 controls batch identity, quantity provenance, seal identity, tamper evidence and release-review authority. It does not itself establish potable status, premium status, regulatory approval or environmental performance.

## Preconditions
1. S6C.7 QMS receipt is accepted.
2. S6C.8 analytical/QMS review is complete to the extent required by the intended product decision.
3. Collection and sample references reconcile to the same event and site.
4. Batch-number and seal-number uniqueness controls are available.
5. Release authority and independent-check requirements are defined.

## Procedure
1. Reconcile event, site, collection, samples and QMS case.
2. Create the unique batch ID and record its creation timestamp.
3. Record quantity only when supported by measurement evidence; otherwise leave quantity unasserted.
4. Bind applicable analytical/QMS result references to the batch.
5. Create and apply a unique seal ID.
6. Record seal application, operator, tamper-evidence status and inspection evidence.
7. Run the release-review checklist against all upstream evidence and deviations.
8. Enter RELEASE_REVIEW_PENDING until the authorized decision is recorded.
9. Preserve the complete batch/seal evidence package and integrity digest.
10. Any material discrepancy places the record on HOLD or FAILED and prevents downstream release.

## Evidence package
- event/site identity
- controlled collection reference
- sample and custody references
- QMS/analysis references
- batch ID and uniqueness evidence
- measured quantity evidence where applicable
- seal ID and application record
- tamper-evidence inspection
- operator/authority identities
- deviations and dispositions
- independent check where required
- integrity digest

## Fail-closed controls
No batch/seal release progression is permitted when upstream QMS evidence is incomplete, identities do not reconcile, quantity is unsupported, seal identity is missing/duplicated, tamper evidence is unresolved, material deviations remain unresolved, or release authority is absent.

## Claim boundary
A batch ID or seal proves traceability of the recorded production object; it does not prove water quality or environmental truth. Premium/product/regulatory release requires the downstream decision framework and evidence.

## Next gate
**S6C.10 — DMRV Package Gate**

Actual product release remains **NOT_RELEASED** until empirical evidence and authorized review are captured.
