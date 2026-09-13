# Blue-Ether Production Commit Sequence

M-1 remains the approved capability milestone. P1-P17 are the production implementation sequence beneath M-1. G-series gates determine acceptance; R is the released state.

## Sequence

| Commit | Production state | Acceptance gate |
|---|---|---|
| P1 | Production foundation | schemas/config/test harness present |
| P2 | Source & weather intelligence | sources, snapshots, provenance |
| P3 | Rainfall event engine | event detection/reconciliation |
| P4 | Production interpolation | volume/capacity/bag planning |
| P5 | Collection orchestrator | first-flush/premium gates |
| P6 | Environmental + water fingerprint | measured/modelled distinction |
| P7 | Premium harvest + batch | quality gate and immutable batch lock |
| P8 | Bottling + instant seal | bottle/seal/hash identity |
| P9 | Evidence + DMRV | manifest, evidence root, lifecycle |
| P10 | ESG/GHG/regulatory | methodology and uncertainty traceability |
| P11 | Blockchain anchoring | reproducible consensus proof |
| P12 | Public verification | QR/batch verification |
| P13 | Investor evidence room | evidence-room completeness |
| P14 | Integrated simulation | failure-path and end-to-end tests |
| P15 | Production readiness | P1-P14 all PASS |
| P16 | Production release | immutable release manifest |
| P17 | **FINAL — Makefile** | reproducible operational entry point |

## Physical production state machine

```text
FORECASTED
 -> COLLECTION_PLANNED
 -> COLLECTION_DEPLOYED
 -> RAIN_EVENT_ACTIVE
 -> FIRST_FLUSH_CONTROLLED
 -> PREMIUM_COLLECTION_ACTIVE
 -> HARVEST_COMPLETE
 -> QUALITY_TEST
 -> QUALITY_PASSED
 -> BATCH_LOCKED
 -> BOTTLED
 -> SEALED
 -> HASHED
 -> ANCHORED
 -> VERIFIED
 -> RELEASED
```

Failure branches are `QUARANTINED` and `REJECTED`. A failed quality gate must never advance a batch to `BATCH_LOCKED`.

## DMRV state machine

```text
RAW -> INGESTED -> QUALITY_CHECKED -> VALIDATED -> CALCULATED
-> EVIDENCE_PACKAGED -> ANCHORED -> VERIFIER_REVIEW -> VERIFIED -> REPORTED
```

## Production assurance rules

1. Forecasts are immutable snapshots and never substitute for measured observations.
2. The 400 L/pod/month value remains a model assumption until empirical validation supports a changed status.
3. Atmospheric measurements are environmental context unless a validated method measures the corresponding property in water.
4. Water-quality release is controlled by measurement/QMS gates, not by blockchain state.
5. Raw sensor data remain off-chain; blockchain anchors evidence roots/proofs.
6. Every investor, ESG, GHG, regulatory and commercial claim must identify source, timestamp, units, methodology version and approval state.
7. `make readiness` must fail if a mandatory production gate fails.
8. `make deploy` must depend on readiness and must never bypass verification.
9. P17 is the final commit in this sequence and contains the repository's reproducible operational command surface.
