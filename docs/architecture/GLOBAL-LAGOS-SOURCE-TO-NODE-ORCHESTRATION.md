# Global Lagos — Source-to-Node Orchestration Contract

## Purpose

Turn the 40-node Global Lagos pilot into an explicit agentic collection-plan surface:

`node × indicator × source × evidence class × cadence × authorization × QC × report family`

The orchestration layer decides what could be collected, from which registered source, at what cadence, under which gate, and into which report families. It does not itself make environmental truth claims.

## Execution states

- `CONTEXT_PLAN`: a registered executable remote/context source can be planned without physical-site authorization.
- `BLOCKED_PENDING_GIS`: a field, measured or verified source is blocked because the node is not authorized in the canonical GIS registry.
- `UNSUPPORTED_ADAPTER`: the source is part of the approved planning vocabulary but does not yet have an executable provider adapter.
- `READY_FOR_AUTHORIZED_COLLECTION` remains reserved for a future state where both authorized GIS and provider/device authorization are positively established.

A public/candidate coordinate is never equivalent to `AUTHORIZED_GIS`.

## Agentic loop

1. Discover node and jurisdiction scope from the canonical 40-node registry.
2. Plan applicable indicators from the Global Lagos data plane.
3. Select only sources bound to the node class and indicator.
4. Check authorization before any field/measured collection.
5. Apply cadence from the indicator and engagement refresh policy.
6. Ingest through registered adapters only.
7. Normalize into canonical observations.
8. QC provenance, timestamp, location, schema and device/custody requirements.
9. Classify evidence without promotion.
10. Evaluate reportability using the canonical reporting engine.
11. Write a reporting snapshot with source versions and evidence packages.
12. Route the resulting snapshot to project, climate, ESG, GHG, grant, investor or audit report families.

## Current adapter boundary

The existing Open-Meteo forecast adapter is the first executable remote adapter. Satellite, air-quality model, local gauge, telemetry, laboratory, GHG activity and ESG-control bindings are represented for coverage and governance, but remain explicitly non-executable until their provider/device contracts and authorization gates are implemented.

## Frontend contract

`/api/global-lagos/orchestration` is a descriptive read model. The frontend can inspect the plan and display collection state, but it cannot promote reportability, authorize a site, or release a reporting snapshot.

## Governance rules

- No city-level coordinate inference.
- No candidate-coordinate promotion.
- No provider output silently promoted from modeled/satellite to measured.
- No physical source collection when GIS authorization is pending.
- No direct provider calls from the frontend.
- No report release from the orchestration plan itself.
