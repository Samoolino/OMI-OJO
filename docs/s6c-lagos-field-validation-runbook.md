# S6C — Controlled Lagos Field Authorization & Premium RainWater Validation Runbook

## 1. Purpose

S6C converts the implemented evidence architecture into a controlled field-validation preparation package for the Global Lagos reference/proof pilot.

It does not authorize physical activity by itself. It does not represent a collector as installed, a rain event as observed, water as harvested, laboratory testing as completed, or Premium RainWater as released.

**Physical status: NOT_RELEASED.**

## 2. Control sequence

```text
SITE AUTHORIZATION
      ↓
SURVEY + GIS CROSS-CHECK
      ↓
COLLECTOR READINESS
      ↓
RAIN-EVENT WATCH
      ↓
FIRST-FLUSH CONTROL
      ↓
CONTROLLED COLLECTION
      ↓
SEALED CONTAINER
      ↓
SAMPLE + CUSTODY
      ↓
WATER-QMS / LAB
      ↓
BATCH + SEAL
      ↓
DETERMINISTIC DMRV PACKAGE
      ↓
EVIDENCE ROOT
      ↓
BLOCKCHAIN ANCHOR
      ↓
PREMIUM-CONDITION REVIEW
      ↓
RELEASE / HOLD
```

Every transition requires evidence appropriate to that transition.

## 3. Gate S6C.1 — Site authorization

Required before equipment is installed or collection occurs:
- documented site/access authorization;
- named responsible authority and authorization reference;
- field safety assessment;
- collection and sampling permissions;
- data/security/privacy permissions where applicable;
- defined public-safe location disclosure boundary.

**No-go:** missing, expired, ambiguous or out-of-scope authorization.

## 4. Gate S6C.2 — Survey and location verification

Use the existing Global Lagos coordinate lifecycle:

```text
REFERENCE_ONLY → SURVEY_REQUESTED → SURVEY_CAPTURED → GIS_CROSSCHECKED → VERIFIED
```

A map point, municipality centroid or public venue record is not automatically a collector coordinate.

Any material mismatch becomes REVIEW_REQUIRED.

Security-sensitive sites must not expose exact operational coordinates publicly.

## 5. Gate S6C.3 — Collector readiness

The first controlled event should use a standardized cleanable collection apparatus.

Readiness evidence should identify:
- collector/catchment configuration;
- cleanability and contamination controls;
- first-flush diversion;
- sealed collection container;
- measurement instruments and qualification/calibration status where applicable;
- synchronized time source;
- operator authorization;
- unique operation ID.

Experimental product containers may be evaluated separately but must not replace the controlled reference apparatus.

## 6. Gate S6C.4 — Rain-event watch

Before collection:
1. record forecast context as FORECAST;
2. identify the authoritative/qualified observation source;
3. record antecedent rainfall context;
4. establish event start/end criteria;
5. confirm collector readiness.

Forecast/model data may support operational watch. They must never be relabeled as measured rainfall.

## 7. Gate S6C.5 — First-flush control

First-flush diversion is a release-critical control.

Record:
- operation ID;
- start time;
- diversion start/end;
- control state;
- operator;
- exceptions;
- evidence reference.

Stop or hold if diversion state is uncertain, contamination occurs, or timestamps are missing.

Reference: docs/W06_Water_Harvesting/WAT-003_First_Flush_Protocol.md.

## 8. Gate S6C.6 — Controlled collection

When the rain event and readiness gates pass:
- open a unique collection operation;
- capture start/end timestamps;
- preserve source/measurement provenance;
- capture collection quantity using the defined measurement method;
- seal the collection container;
- generate collection evidence immediately;
- preserve original records append-only.

Corrections are successor records, never silent overwrites.

## 9. Gate S6C.7 — Sampling and custody

Each sample must be traceable to the collection operation and, later, the batch.

```text
SAMPLE_ID → CONTAINER_ID → COLLECTION_OPERATION → CUSTODY_TRANSFER → LAB_RECEIPT → TEST_RESULT → BATCH
```

A broken chain blocks Premium release.

## 10. Gate S6C.8 — Water-QMS / laboratory review

The applicable laboratory/QMS method must be selected before testing.

Evidence must retain:
- laboratory identity/provenance;
- method/reference;
- sample identity;
- collection and receipt times;
- result units;
- quality controls;
- exceptions;
- reviewer status.

No potable or consumer-safety claim is permitted merely because a sample was collected or anchored.

## 11. Gate S6C.9 — Batch and seal provenance

Before product release:
- assign a unique batch ID;
- reconcile collection and sample references;
- assign container/seal identifiers;
- record quantity and timestamps;
- generate batch provenance hash;
- assign release reviewer.

Mismatch => HOLD.

## 12. Gate S6C.10 — DMRV package

Construct the deterministic evidence package from the available records.

Required relationships:

```text
Rain Event → Collection → First Flush → Sample/Custody → Water-QMS → Batch/Seal → DMRV Review
```

Canonicalize using the established evidence-package rules and compute the evidence root.

## 13. Gate S6C.11 — Blockchain anchor

Anchor only the deterministic evidence root.

The chain can support:
- timestamp/inclusion evidence;
- digest integrity;
- anchor transaction traceability;
- independent verification.

The chain does not establish:
- rainfall truth;
- water quality;
- potability;
- ESG/GHG performance;
- regulatory approval;
- grant eligibility.

## 14. Gate S6C.12 — Premium-condition review

Premium classification remains evidence-dependent.

Minimum review set:
- rain event;
- antecedent rainfall;
- atmospheric context;
- collection integrity;
- first-flush record;
- sample/custody;
- applicable water-QMS;
- batch provenance;
- seal integrity;
- DMRV review.

If any material element is missing or contradictory, the state is HOLD.

## 15. Fail-closed matrix

| Condition | State | Action |
|---|---|---|
| Authorization missing | HOLD | No physical activity |
| Site not verified | HOLD | Complete survey/GIS cross-check |
| Forecast only | REPORTABLE/FORECAST | Do not call measured |
| First-flush uncertain | HOLD | Do not release collection |
| Missing custody event | HOLD | Do not release batch |
| QMS exception unresolved | HOLD | Review before claim |
| Batch/seal mismatch | HOLD | Reconcile |
| Conflicting sources | HOLD | Independent review |
| Blockchain anchor absent | REVIEW/HOLD | Do not claim anchored |
| Public-safe boundary breached | HOLD | Remove/restrict exposure |

## 16. Evidence-state semantics

REPORTABLE is not the same as MEASURED.

The controlled ladder remains:

```text
REPORTABLE → VALIDATED → VERIFIED → ANCHORED
```

Evidence classes remain:
- OBSERVED
- FORECAST
- MODELLED
- SATELLITE
- CALCULATED
- PROXY

## 17. S6C release authority

S6C cannot self-authorize field operations.

Promotion requires:
1. authorization evidence;
2. independent site/location check;
3. collector readiness record;
4. QMS/lab readiness;
5. safety review;
6. named release authority;
7. recorded hold/rollback conditions.

Until those artifacts exist, the production manifest remains NOT_RELEASED.

## 18. Controlled pilot outputs

The intended first controlled evidence package is:
- authorized site record;
- verified field location;
- collector readiness;
- rain-event record;
- first-flush record;
- collection record;
- sample/custody record;
- QMS/lab evidence;
- batch/seal record;
- deterministic DMRV package;
- evidence root;
- blockchain receipt when controlled deployment is complete;
- Premium-condition review record.

This sequence is the bridge between the existing digital evidence system and an eventual authorized physical Premium RainWater demonstration.
