# S6C.6 — Lagos Controlled Collection and Sample Capture Runbook

## Objective
Execute a bounded controlled collection after S6C.5 first-flush eligibility and create traceable samples for downstream custody/QMS review.

## Preconditions
1. S6C.5 is accepted for the same rain event and site.
2. Field authorization remains valid.
3. Site and collector identities match the approved records.
4. Collection container/vessel identity and integrity are verified.
5. Sampling plan and sample identifiers are prepared.
6. Operator identity, communications and safety checks are recorded.
7. Time sources are synchronized.

## Procedure
1. Create the S6C.6 record and bind it to the S6C.5 event/control reference.
2. Verify site, collector, container and sampling-plan identities.
3. Record the collection start timestamp before controlled collection begins.
4. Enter COLLECTION_ACTIVE and record the operator action.
5. Collect only within the approved controlled window and container configuration.
6. Record measured volume where an approved instrument is available.
7. Capture uniquely identified samples using the approved sampling plan; record each sample ID and capture timestamp.
8. Record collection completion and enter COLLECTION_COMPLETE.
9. Confirm sample/container integrity and enter SAMPLE_CAPTURED only when traceability is complete.
10. Preserve the evidence package and integrity digest for S6C.7 custody/QMS handoff.

## Evidence package
The package must contain the S6C.5 reference, site/collector/container identity, collection timestamps, volume evidence where applicable, sample IDs and timestamps, sampling-plan revision, operator log, applicable instrument/calibration references and an integrity digest.

## Fail-closed controls
Stop and hold the event if authorization is missing/expired, S6C.5 was not accepted, identities do not match, sample IDs are missing/duplicated, container integrity is compromised, instrumentation or timing fails, contamination is suspected, conditions become unsafe, or provenance/integrity evidence is incomplete.

## Gate interpretation
SAMPLE_CAPTURED means traceable physical samples were recorded under this control gate. It does **not** establish laboratory results, potable/safe status, premium status, a released batch, regulatory approval or verified environmental benefit.

## Next gate
**S6C.7 — Sampling Custody and QMS Handoff**

Actual field execution remains NOT_RELEASED until empirical evidence is captured and independently reviewed.
