# S6C.2 — Lagos Survey & GIS Verification Runbook

## Control objective

Establish a reproducible location-verification gate for the Global Lagos controlled field-validation path without fabricating coordinates, disclosing security-sensitive exact locations, or treating a site reference as physical authorization.

**Current physical status:** NOT_RELEASED.

## Prerequisite

S6C.1 must have an independently reviewed decision of **ACCEPTED** with valid, in-scope authorization evidence.

S6C.2 acceptance does not authorize collection, bottling, product release, potability claims, environmental-credit claims, or regulatory approval.

## Controlled sequence

`REFERENCE_ONLY → SURVEY_REQUESTED → SURVEY_CAPTURED → GIS_CROSSCHECKED → VERIFIED`

A material mismatch routes to:

`GIS_CROSSCHECKED → REVIEW_REQUIRED → GIS_CROSSCHECKED`

No state may bypass the sequence.

## Required evidence

1. Accepted S6C.1 decision reference.
2. Survey request ID and authorized scope.
3. Surveyor identity and method.
4. Capture timestamp.
5. Coordinate system and provenance.
6. Survey capture record.
7. Authoritative GIS source and cross-check result.
8. Independent checker.
9. Public-safe location representation.
10. Resolution record for any material mismatch.

## Coordinate integrity rules

- Never invent or interpolate an exact site coordinate.
- A reference coordinate is not a surveyed coordinate.
- A survey capture is not independently verified.
- Verification requires an authoritative GIS cross-check.
- A material mismatch remains **REVIEW_REQUIRED** until resolved and rechecked.
- Exact coordinates for security-sensitive sites remain restricted.
- Public and investor surfaces expose only the approved public-safe representation.

## Evidence-state semantics

| State | Meaning |
|---|---|
| REFERENCE_ONLY | Location is a planning/reference record; no survey evidence exists. |
| SURVEY_REQUESTED | A controlled survey request exists within an accepted scope. |
| SURVEY_CAPTURED | Survey evidence has been captured with timestamp/provenance. |
| GIS_CROSSCHECKED | Authoritative GIS comparison and independent check are recorded. |
| VERIFIED | Cross-check passed and no unresolved material discrepancy remains. |
| REVIEW_REQUIRED | A discrepancy or evidence defect prevents verification. |

## Fail-closed conditions

The gate remains HOLD/REVIEW_REQUIRED for:

- missing or unaccepted S6C.1 authorization evidence;
- expired or out-of-scope authorization;
- unverifiable survey provenance;
- missing capture timestamp;
- missing coordinate system;
- missing authoritative GIS source;
- missing independent checker;
- material coordinate mismatch;
- unauthorized disclosure of a sensitive exact location.

## Release boundary

A verified location is an evidence prerequisite for later controlled readiness gates. It is **not** evidence that a collector has been installed, rainwater has been harvested, a sample has been tested, a batch has been produced, or a product has been released.

The physical chain remains:

`SITE AUTHORIZATION → SURVEY/GIS VERIFICATION → COLLECTOR READINESS → RAIN EVENT → FIRST FLUSH → CONTROLLED COLLECTION → SAMPLING/CUSTODY → WATER-QMS → BATCH/SEAL → DMRV → ANCHOR → PREMIUM CONDITION REVIEW`

## Evidence integrity

Records should be canonically serialized as UTF-8 JSON with lexicographically sorted object keys, declared array order preserved, and SHA-256 used for deterministic integrity checks.

Corrections are append-only successor records; prior records are not overwritten.

## Gate decision

S6C.2 may transition to **VERIFIED** only when all required evidence is present, internally consistent, independently checked, and within authorization scope.

**Next gate:** S6C.3 — Collector Readiness Gate.
