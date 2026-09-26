# Illovediza Fuerza — ES-6 DMRV Indicator Mapping & Evidence Package

## Objective

Transform reconciled Spanish node observations into deterministic DMRV records and evidence packages suitable for controlled ESG/GHG reporting, review and later blockchain anchoring.

## DMRV layers

1. **Observation layer** — original provider record and source metadata.
2. **Normalization layer** — canonical units, timestamps and spatial identifiers.
3. **Quality layer** — provider flags, completeness and validation checks.
4. **Reconciliation layer** — cross-source relationship and conflict state.
5. **Indicator layer** — methodology-defined indicator and calculation context.
6. **Evidence layer** — evidence class, provenance and supporting records.
7. **Package layer** — deterministic canonical package and SHA-256 root.
8. **Anchor layer** — optional blockchain transaction referencing the package root.
9. **VDR layer** — human-readable and machine-readable evidence index.

## Environmental indicator mapping

### Rainfall

Keep observed rainfall and forecast rainfall separate. Forecast accuracy is a derived validation indicator requiring later observed values and a documented comparison window.

### Atmospheric and weather indicators

Temperature, humidity, pressure, wind and atmospheric-moisture indicators retain source, method, unit and timestamp. Derived indicators must reference their calculation method.

### Air quality

NO2, O3, PM2.5, PM10, SO2 and CO retain station/model identity and measurement class. Cross-source relationships are stored separately from the underlying records.

### Remote sensing

Satellite/model products remain remote-sensing/model evidence and are not represented as ground measurements unless an explicit validation method supports that interpretation.

### Water and physical operations

Collection volume, first-flush state, sample custody, water-quality results, batch identity and seal state become DMRV evidence only after the physical production procedure generates them.

### ESG/GHG

Calculated emissions require a documented activity value, emission-factor source/version, calculation method and uncertainty/assumption record where applicable. The DMRV package stores the calculation lineage rather than only the final number.

## Canonical package

A package contains:

- package identifier
- node identifiers
- evidence records
- source registry references
- methodology/version references
- quality and reconciliation results
- exceptions and resolutions
- calculation lineage
- generated-at timestamp
- schema version
- successor/supersession relationships

Canonical serialization must be deterministic before SHA-256 hashing.

## Blockchain boundary

The package hash/root can be anchored to a supported blockchain registry. The transaction is a tamper-evidence reference. It does not transform a reportable observation into a verified environmental fact.

## Institutional acceptance criteria

ES-6 passes when a test package can be reconstructed from its source records; canonicalization produces the same hash for identical inputs; material changes produce a different hash; provenance survives packaging; evidence classes are preserved; and dashboard presentation cannot alter the underlying evidence state.

## Next gate

`S6A / ES-9 — Controlled blockchain evidence registry and public verification.`
