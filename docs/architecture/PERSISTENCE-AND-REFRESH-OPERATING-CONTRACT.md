# UB-02 Persistence and Refresh Operating Contract

## Purpose
Define the production boundary for continuous Climate & ESG reporting without coupling the reporting domain to a particular database, cloud vendor, or cron provider.

## Canonical lifecycle
PROJECT CONTRACT → REFRESH POLICY → SOURCE ADAPTER → CANONICAL OBSERVATIONS → DURABLE OBSERVATION STORE → QC / LOCATION / TIME / RECONCILIATION → REPORTABILITY → VERSIONED REPORTING SNAPSHOT → DURABLE SNAPSHOT STORE → RELEASE GATE → REPORT / dMRV / VDR / AUDIT

## Persistence requirements
A production adapter MUST provide:
1. idempotent observation writes;
2. immutable source/provenance metadata;
3. historical observation retrieval;
4. immutable/versioned snapshot storage;
5. deterministic snapshot hash retention;
6. project/site/indicator/time indexes;
7. explicit failure handling;
8. no silent overwrite of released evidence.

The domain interface is src/reporting/persistence_contract.py.

## Refresh requirements
The scheduler MUST:
- read the engagement registry;
- respect declared cadence;
- invoke only approved source adapters;
- pass observations through the same reportability engine;
- persist before release;
- record refresh success/failure;
- avoid duplicate observations;
- never infer missing physical coordinates;
- never promote remote/modelled data to measured evidence.

The web endpoint /api/reporting/refresh is a scheduler boundary, not itself a durable job queue.

## Release states
DRAFT → REVIEW → APPROVED → RELEASED

Exceptions remain outside release: QUARANTINED, STALE, OUT_OF_BOUNDARY, SOURCE_UNAPPROVED, REJECTED.

A scheduler may create a DRAFT snapshot. It must not bypass human/project release gates merely because source retrieval succeeded.

## Deployment adapter decision
The repository currently does not declare a production database dependency. Therefore the canonical reporting domain uses a persistence interface rather than introducing an arbitrary provider.

A deployment may implement that interface with its approved relational or managed data service. The adapter must be selected and provisioned as part of the deployment architecture, with credentials supplied through the deployment secret manager.

## Evidence boundary
Remote/modelled observations may support contextual reporting where a project contract permits it. They do not become measured or verified evidence merely because they are persisted, scheduled, hashed, or blockchain-anchored.

Blockchain anchoring, where enabled by an engagement, certifies integrity of a released evidence package; it does not certify environmental truth.