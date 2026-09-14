# Blue-Ether DMRV Portal

**State:** S3 — IMPLEMENTED (controlled integration baseline)

This portal is the authorized DMRV interface for government, ESG clients and auditors. The implementation boundary is deliberately evidence-first: raw telemetry and laboratory evidence remain off-chain; the chain stores hashes, state, timestamps, LCDA identity and verifier identity.

## Implemented integration

- `src/contracts/BlueEtherDMRVRegistry.sol` — role-gated evidence registry.
- `app.js` — browser-safe SHA-256 canonicalization module for evidence payloads.
- `dmrv-evidence.schema.json` — canonical observed-evidence contract.

## Required production conditions

1. **Observed-only DMRV:** the contract rejects `FORECAST` submissions. Forecasts can support logistics and planning but cannot become measured production evidence.
2. **Provenance:** each record must have a deterministic evidence ID, payload hash, source hash and metadata hash.
3. **Temporal integrity:** `observedAt` must be non-zero and cannot be in the future relative to the anchoring transaction.
4. **Duplicate protection:** an evidence ID can be submitted only once.
5. **Separation of duties:** submitters and verifiers are separate role classes; verification is an explicit second state transition.
6. **Pause control:** the owner can pause new state transitions during incident response.
7. **Quality boundary:** water-quality/QMS evidence is referenced by hash and status; the registry does not certify laboratory results.
8. **Financial boundary:** DMRV evidence is not automatically financial recognition. The 400 L/pod/month value remains a model assumption until observed data and signed technical review support an upgrade.

## Integration sequence

```text
AWS IoT Greengrass / field sensors
        │
        ├── observed telemetry
        ▼
Ingestion + validation service
        │  calibration / unit checks / anomaly quarantine
        ▼
Canonical evidence JSON
        │
        ├── SHA-256(payload)
        ├── SHA-256(source reference)
        └── SHA-256(metadata)
        ▼
DMRV Registry submitEvidence()
        │
        ▼
SUBMITTED → independent VERIFIER → VERIFIED / REJECTED
        │
        ▼
Audit package: raw evidence + hashes + tx receipt + QMS references
```

## Deployment / verification gate

Do not mark this component S4 or S5 merely because the Solidity compiles. Before controlled production use, verify:

- contract deployment address and chain ID recorded in a versioned registry;
- role assignments reviewed and least-privilege tested;
- unit/integration tests cover duplicate, future timestamp, unauthorized role, paused state and forecast rejection;
- rainfall observations reconciled against the approved historical/reference dataset;
- sensor calibration and QMS evidence attached to the same evidence lineage;
- at least one end-to-end controlled-fork attestation is retained;
- audit export reproduces the exact payload hash from the stored source artifact.

## Claim boundary

The DMRV portal never converts a forecast into a measured value and never treats an on-chain hash as proof that an underlying physical measurement is scientifically correct. The chain proves integrity of the submitted evidence package and its verification history; scientific validity remains governed by calibration, sampling, QMS and review controls.
