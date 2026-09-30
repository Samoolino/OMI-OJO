# S6C.7 — Lagos Sampling Custody and QMS Handoff Runbook

## Objective
Maintain a defensible chain of custody from S6C.6 sample capture through documented QMS intake, preserving sample identity, condition and provenance for downstream analysis.

## Preconditions
1. S6C.6 is accepted for the same event and site.
2. Every sample has a unique identifier.
3. Sample and container identities reconcile with the collection record.
4. Applicable seal/integrity identifiers are recorded.
5. Custodians and destination QMS recipient are identified.
6. Required storage and transport conditions are defined.
7. Time sources are synchronized.

## Procedure
1. Create the S6C.7 custody record and bind it to the S6C.6 reference.
2. Reconcile sample IDs, container IDs and applicable seals before transfer.
3. Record origin custodian acceptance and enter CUSTODY_READY/IN_CUSTODY.
4. Record each custody transfer with sender, receiver, timestamp, identity and sample/container set.
5. Record storage and transport conditions and any applicable temperature evidence.
6. Inspect condition on receipt and record deviations or nonconformances.
7. Obtain documented QMS intake acknowledgement.
8. Enter QMS_RECEIVED only when identity, custody and intake evidence are complete and material deviations have an approved disposition.
9. Preserve the custody evidence package and integrity digest for S6C.8.

## Evidence package
The package must contain the S6C.6 reference, sample/container reconciliation, seal or integrity condition, custody transfers, timestamps, custodian identities, storage/transport conditions, receipt condition, deviations/dispositions, QMS acknowledgement and integrity digest.

## Fail-closed controls
Place the record on HOLD or FAILED for missing upstream acceptance, identity mismatch, broken/unexplained seal condition, unidentified custodian, unexplained custody gaps, storage/transport excursions without disposition, missing QMS acknowledgement, unresolved material deviations, or incomplete provenance.

## Gate interpretation
QMS_RECEIVED means the designated QMS function has documented receipt under the defined custody controls. It does **not** mean laboratory analysis passed, water is potable or premium, a batch is released, or regulatory/environmental claims are verified.

## Next gate
**S6C.8 — QMS/Lab Analysis Readiness**

Actual custody and QMS intake remain NOT_RELEASED until empirical records are captured and independently reviewed.
