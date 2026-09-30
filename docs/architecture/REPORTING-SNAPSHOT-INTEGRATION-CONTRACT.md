# Reporting Snapshot Integration Contract

The governed reporting runtime now uses the following boundary:

DISCOVER → PLAN → GATE → EXECUTE → NORMALIZE → QC → EVIDENCE PACKAGE → REPORTABILITY → DRAFT SNAPSHOT → PERSISTENCE

## Refresh behavior

A refresh run:

1. receives canonical observations from the source/orchestration layer;
2. builds the approved source union from the engagement rules;
3. runs evidence QC;
4. creates a deterministic evidence package containing both accepted and exception decisions;
5. passes only QC-passed observations into the reportability engine;
6. persists only those observations to the canonical observation store;
7. builds a deterministic reporting snapshot;
8. persists the snapshot as DRAFT.

## Important boundaries

- QC-passed does not automatically mean REPORTABLE.
- MODELED remains MODELED; evidence class is never promoted by refresh.
- CONTEXTUAL_ONLY, STALE, OUT_OF_BOUNDARY, SOURCE_UNAPPROVED, QUARANTINED, and REJECTED observations do not enter the reportable observation set.
- Snapshot creation does not release a report.
- Persistence does not release a report.
- Production release remains a separate governed state transition.

## Auditability

The refresh result now exposes:

- evidence_package_id
- qc_decisions
- reportability decision count
- snapshot ID
- deterministic snapshot hash
- next scheduled refresh

This creates a traceable chain from collection through evidence processing to the reporting read model.

## Global Lagos

The current executable adapter remains Open-Meteo forecast/context data. Physical and specialized source bindings remain gated until their authorization, adapter, custody and QC contracts are implemented.
