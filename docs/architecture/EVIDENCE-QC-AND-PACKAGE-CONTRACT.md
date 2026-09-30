# Evidence QC and Package Contract

## Purpose

This layer sits between agentic collection and reportability:

DISCOVER → PLAN → GATE → EXECUTE → NORMALIZE → QC → EVIDENCE PACKAGE → REPORTABILITY → SNAPSHOT

The processor creates a decision ledger and a deterministic evidence-package manifest. It does not release reports and it does not upgrade evidence classes.

## QC gates

1. Source authorization — source must belong to the approved source set.
2. Provenance — provider, source snapshot and methodology status are required.
3. Schema/value integrity — units are present and numeric observations must be finite.
4. Time integrity — timestamps must carry timezone information and be within the evidence freshness window.
5. Spatial integrity — WGS84 coordinates must be valid; when an authorized location is supplied, the observation must fall within the configured tolerance.
6. Evidence-class preservation — QC never changes CONTEXTUAL, MODELED, SATELLITE, MEASURED or VERIFIED_MEASUREMENT.
7. Explicit exception states — failures become SOURCE_UNAPPROVED, QUARANTINED, STALE, OUT_OF_BOUNDARY or REJECTED; they are not silently discarded.

## Evidence package

Each package contains:

- deterministic package ID and SHA-256 hash;
- observation IDs;
- source IDs;
- evidence classes;
- QC-passed and quarantined IDs;
- decision IDs;
- methodology assertions.

The package hash covers canonical sorted content and is stable for the same evidence set and methodology.

## Reportability boundary

Only observations with QC_PASSED are passed to the reportability engine. Reportability can still return CONTEXTUAL_ONLY, SOURCE_UNAPPROVED, STALE, OUT_OF_BOUNDARY or another terminal/non-release state.

QC is necessary but not sufficient for publication.

## Current Global Lagos position

The current executable source remains Open-Meteo forecast/context collection. Physical gauges, telemetry, water-lab results, GHG activity data and ESG control records remain gated behind their authorization and adapter contracts. Candidate public coordinates do not satisfy that gate.

The frontend reads reporting read models; it does not promote evidence or call providers directly.
