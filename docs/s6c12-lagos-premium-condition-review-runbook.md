# S6C.12 — Lagos Premium Condition Review Gate Runbook

## Objective
Determine whether a specific rainwater batch satisfies the project's defined premium-condition criteria using traceable evidence across the physical collection, water/QMS, DMRV and integrity chain.

## Preconditions
1. Rain-event evidence is traceable to the same site and event.
2. First-flush control and controlled collection records are complete.
3. Sampling/custody evidence reconciles.
4. Applicable laboratory/QMS evidence is available and reviewed.
5. Batch and seal identities reconcile.
6. The DMRV package is accepted.
7. The required blockchain anchor reference is available where policy requires anchoring.
8. The premium criteria revision and acceptance criteria are fixed for the review.
9. Regulatory/product-release requirements are separately identified.

## Procedure
1. Create a unique premium-review ID and bind it to the exact batch.
2. Freeze the criteria revision used for the decision.
3. Reconcile the full evidence chain from rain event through batch/seal and DMRV.
4. Evaluate each premium criterion independently.
5. Record evidence references and acceptance criteria for every criterion.
6. Record all deviations and their dispositions.
7. Apply an independent review where required.
8. Record one of the defined review outcomes.
9. Preserve the decision record and integrity digest.
10. If any material criterion lacks sufficient evidence, do not infer premium status; place the case on HOLD or PREMIUM_NOT_ESTABLISHED.

## Decision semantics

### PREMIUM_REVIEW_READY
All prerequisite evidence and criteria definitions are present, but review has not yet been completed.

### PREMIUM_REVIEW_IN_PROGRESS
Criterion-by-criterion evaluation is underway.

### PREMIUM_ELIGIBLE_PENDING_RELEASE
The defined premium-condition criteria have been supported by the recorded evidence, but this state does not itself authorize commercial or regulatory product release.

### PREMIUM_NOT_ESTABLISHED
The evidence does not establish the defined premium condition, or required evidence is incomplete.

### HOLD / FAILED
A material control, provenance, integrity, identity or review condition has failed or remains unresolved.

## Evidence boundary
Rainfall opportunity alone cannot establish premium rainwater. A blockchain anchor establishes integrity/traceability of the anchored evidence root; it does not establish water quality or environmental truth.

Forecast, modelled and proxy indicators remain explicitly classified and cannot be represented as observations.

## Release boundary
Even an outcome of PREMIUM_ELIGIBLE_PENDING_RELEASE requires the separate applicable regulatory/product-release authority and release criteria before any public commercial claim or physical release.

## Next gate
**POST-S6C — Release Authorization and Public Verification**

Physical/product status remains **NOT_RELEASED** until empirical evidence and authorized release are recorded.
