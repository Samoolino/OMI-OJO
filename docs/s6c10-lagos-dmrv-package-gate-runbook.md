# S6C.10 — Lagos DMRV Package Gate Runbook

## Objective
Assemble a deterministic, evidence-linked DMRV package that binds the physical batch to environmental observations, water/QMS records, calculations, models and ESG/GHG reporting inputs without collapsing different evidence classes.

## Scope
S6C.10 is the evidence-packaging and review gate. It is not itself a blockchain anchor, premium decision, regulatory release or independent environmental verification.

## Preconditions
1. S6C.7 custody/QMS receipt is accepted.
2. S6C.8 analytical/QMS evidence is sufficiently complete for the intended package.
3. S6C.9 batch/seal records reconcile to the same event and site.
4. All material evidence has source, timestamp and provenance.
5. Calculations and models have method/version references.
6. Material claim statements can be mapped to evidence.

## Procedure
1. Create a unique DMRV package ID.
2. Bind event, site, collection, first-flush, sample/custody, QMS, batch and seal records.
3. Register every material environmental evidence item with its evidence class.
4. Preserve source identifiers, timestamps, location/grid, provider/method revision and quality status.
5. Record transformations, calculations and model versions.
6. Register ESG/GHG indicators with their evidence and calculation references.
7. Create a claim register; every material claim must point to supporting evidence.
8. Reconcile conflicting sources. Do not silently average or discard material conflicts.
9. Generate a deterministic package digest.
10. Move to INDEPENDENT_REVIEW_PENDING; verification must be separately recorded.

## Evidence classes
Use only the defined classes: OBSERVED, FORECAST, MODELLED, SATELLITE, CALCULATED and PROXY. Forecasts cannot be represented as observations. Modelled/proxy evidence retains its classification.

## Fail-closed controls
Hold or fail when provenance is missing, evidence classes are ambiguous, material source conflicts remain unresolved, calculation/model versions are absent, claims lack evidence linkage, upstream identities do not reconcile, or package integrity cannot be established.

## Claim boundary
A DMRV package demonstrates traceable evidence assembly. It does not by itself prove environmental truth, potable water, premium status, regulatory approval or GHG reduction. A blockchain hash later proves integrity of the package presented for anchoring, not truth of its contents.

## Next gate
**S6C.11 — Blockchain Anchor Gate**

Physical/product status remains **NOT_RELEASED** until all required empirical, review and authorization gates are satisfied.
