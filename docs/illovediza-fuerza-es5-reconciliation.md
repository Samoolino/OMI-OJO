# Illovediza Fuerza — ES-5 Reconciliation & Non-Contradiction Runtime

## Objective

Convert configured Spanish environmental feeds into controlled reportable evidence without silently merging incompatible observations, forecasts, stations, models, units or timestamps.

## Evidence state machine

`RECEIVING -> NORMALIZED -> QUALITY_CHECKED -> SPATIALLY_ALIGNED -> TEMPORALLY_ALIGNED -> CROSS_SOURCE_RECONCILED -> REPORTABLE`

Any material failure becomes `EXCEPTION_REVIEW` and cannot promote to `REPORTABLE` until resolved or explicitly qualified.

## Required evidence tuple

Every observation must carry:

- node_id
- provider_id
- source_record_id
- indicator
- value
- unit
- observed_at
- retrieved_at
- spatial_reference
- method/source class
- quality state
- provenance
- evidence class
- schema/version

## Cross-source rules

### Rainfall

Do not compare a municipal forecast directly against a station observation as though both were measurements. Preserve `FORECAST` and `OBSERVATION` classes and compare only through an explicit forecast-validation record.

### Air quality

NO2, O3, PM2.5 and related indicators require spatial/station identity, timestamp and measurement/model class. A station reading and a model grid estimate remain distinct evidence records. Agreement can create a `QUALIFIED_CROSS_SOURCE` relationship; it does not replace either source.

### Atmospheric/weather indicators

Temperature, humidity, pressure, wind and related measurements require compatible units and timestamps. Missing or stale values are flagged rather than imputed silently.

## Non-contradiction checks

1. identity compatibility
2. unit conversion validity
3. timestamp window
4. spatial distance / grid relationship
5. provider quality flags
6. observation versus model/forecast class
7. methodology compatibility
8. provenance completeness
9. duplicate detection
10. supersession/version integrity

## Conflict policy

`CONFLICT -> FAIL_CLOSED -> EXCEPTION_RECORD -> REVIEW -> RESOLUTION_OR_QUALIFICATION`

The system must never average contradictory sources merely to produce a clean dashboard number.

## Reportability

A value may be `REPORTABLE` only when provenance, units, timestamp, spatial identity and quality checks pass. `REPORTABLE` does not mean independently verified.

## DMRV handoff

A reconciled record can enter the DMRV evidence package with its source lineage intact. The package receives a deterministic canonical representation and evidence hash. Only the package root is eligible for blockchain anchoring.

## Institutional acceptance

ES-5 is complete when test fixtures demonstrate:

- compatible sources reconcile;
- forecast and observation remain semantically distinct;
- conflicting sources fail closed;
- unit mismatches fail closed;
- stale observations are qualified;
- corrections are append-only successors;
- evidence hashes change when material source data changes;
- dashboard presentation cannot upgrade evidence state.

## Next gate

`ES-6 — DMRV indicator mapping and evidence-package generation.`
