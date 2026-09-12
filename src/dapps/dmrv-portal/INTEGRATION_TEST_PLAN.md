# DMRV integration test plan

## Gate A — Contract invariants

- Unauthorized address cannot submit evidence.
- Unauthorized address cannot verify evidence.
- Forecast-class evidence reverts with `FORECAST_NOT_DMRV`.
- Duplicate `evidenceId` reverts with `DUPLICATE_EVIDENCE`.
- Future `observedAt` reverts with `INVALID_OBSERVED_AT`.
- Zero payload/evidence/LCDA identifiers are rejected.
- Paused registry rejects state transitions.

## Gate B — Data lineage

For every test observation, retain:

1. canonical JSON payload;
2. payload SHA-256;
3. source artifact hash;
4. metadata hash;
5. sensor/device identifier;
6. calibration/QMS reference;
7. LCDA identifier;
8. observation timestamp;
9. transaction hash;
10. verifier address and verification timestamp.

## Gate C — Rainfall/yield reconciliation

The DMRV record must distinguish:

- measured rainfall;
- measured harvested volume;
- first-flush loss;
- rejected volume;
- storage-constrained volume;
- forecast rainfall/yield.

Forecast values are never copied into the measured fields.

## Gate D — Controlled-fork attestation

Run the full evidence lifecycle on the approved controlled fork:

`OBSERVED PAYLOAD → HASH → SUBMIT → VERIFY → EXPORT → REHASH`

Acceptance criterion: the exported canonical payload reproduces the original payload hash exactly and the on-chain record contains the expected LCDA, observed timestamp and state transition.

## Gate E — Production readiness

S4 requires passing Gates A-D plus signed technical review. S5 requires operational ownership, monitoring, incident response and an approved production deployment record.
