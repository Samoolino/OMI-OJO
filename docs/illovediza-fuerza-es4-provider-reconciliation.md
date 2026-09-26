# Illovediza Fuerza — ES-4 Provider & Reconciliation Gate

## Objective

Move Spain municipality nodes from administrative/reporting readiness toward controlled environmental feed readiness without overstating live data.

## Authoritative starting point

AEMET OpenData provides REST access to reusable meteorological/climatological data and documents programmed API access. Current AEMET documentation also exposes daily and hourly municipal forecast endpoints. API keys are required and must be managed server-side with expiry/rotation controls.

The Spanish official data catalogue also exposes an air-quality station registry/service. The registry is not treated as a live measurement feed until its measurement endpoint, schema, update cadence and provenance are explicitly bound and tested.

## Feed classes

- `POLLING_API`: periodic retrieval from an API
- `PUSH_STREAM`: source actively pushes observations
- `ARCHIVE_QUERY`: historical retrieval
- `MODEL`: modelled/forecast output
- `SATELLITE`: remotely sensed product
- `MANUAL`: controlled human entry

The class is part of the observation provenance and cannot be inferred from a dashboard appearance.

## Minimum observation envelope

Every observation entering the canonical evidence layer must retain:

- provider
- source record identifier
- observed timestamp
- retrieval timestamp
- spatial reference/station identifier
- variable
- value
- unit
- method/class
- quality state
- source/version metadata

## Reconciliation

Before a value becomes `REPORTABLE`, the runtime evaluates:

1. time compatibility;
2. spatial compatibility;
3. unit normalization;
4. duplicate detection;
5. missingness and completeness;
6. provider provenance;
7. method compatibility;
8. quality flags;
9. forecast-versus-observation distinction.

A forecast must never be silently converted into an observation. A station measurement must not be reassigned to a municipality merely because it is geographically nearby without preserving the station relationship and spatial method.

## Cross-source rule

Where two sources report the same indicator, the system does not automatically average them. It creates a reconciliation record with source-specific values, time/spatial relationship, uncertainty/quality metadata and an outcome of `AGREE`, `QUALIFIED`, or `EXCEPTION_REVIEW`.

Material conflict is fail-closed.

## Live-feed promotion

`CONFIGURED` means credentials/endpoints/schema are registered.

`RECEIVING` means successful runtime retrieval has occurred.

`RECONCILED` means canonical validation passed.

`REPORTABLE` means the observation satisfies the defined reporting rules. None of these states alone means independent verification.

## Credentials

Provider API keys remain server-side secrets. The frontend receives normalized observations and provenance, never provider credentials.

## Acceptance gate

ES-4 is complete for an indicator/provider pair only after a controlled retrieval, schema validation, provenance capture, timestamp/coordinate/unit checks, failure handling, and reconciliation test have passed.

## Next gate

`ES-5 — multi-source reconciliation implementation and non-contradiction runtime.`
