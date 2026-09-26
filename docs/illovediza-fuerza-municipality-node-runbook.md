# Illovediza Fuerza — Spain Municipality Node Runbook

## Purpose

Bind every Spanish municipality to the common Blue-Ether reporting-node contract without implying that a physical collector, environmental sensor, rainwater harvest, or verified environmental claim exists at that municipality.

## Node lifecycle

`ADMINISTRATIVE -> REPORTING_READY -> FEED_UNCONFIGURED -> FEED_CONFIGURED -> RECEIVING -> RECONCILED -> REPORTABLE -> VALIDATED -> VERIFIED -> ANCHORED`

Physical states remain separate:

`SITE_UNAUTHORIZED -> SITE_AUTHORIZED -> COLLECTOR_READY -> COLLECTION_EVENT -> SAMPLE_CUSTODY -> QMS_REVIEW -> BATCH_REVIEW -> RELEASE_REVIEW`

## Required municipality record

- official municipality name
- official INE municipality code
- province
- autonomous community/city
- authoritative administrative source/version
- geometry/centroid source
- coordinate precision and provenance
- provider bindings
- indicator availability
- evidence class
- timestamp
- units
- quality state
- reconciliation state
- evidence package/hash when created

## Feed policy

Do not mark a source as live merely because an API exists. The runtime must classify transport as `PUSH_STREAM`, `POLLING_API`, `ARCHIVE_QUERY`, `MODEL`, `SATELLITE`, or `MANUAL` according to the actual documented transport.

Every configured indicator requires provider provenance, timestamp, unit, methodology, quality status and reconciliation rules before it can become `REPORTABLE`.

## Geographic integrity

Municipality nodes are reporting anchors. A node becomes a physical harvest site only after an explicit site authorization record and verified site coordinates. Municipality centroid coordinates must never be represented as a physical collector location.

## Non-contradiction

Conflicts are fail-closed. The system does not blindly average providers. Material discrepancies create an exception record and require resolution or qualification. Corrections are append-only successor records.

## Premium RainWater

No municipality node may display a Premium RainWater claim merely because rainfall is observed there. Premium classification requires the physical-production gate: authorized site, collection integrity, first-flush record, sampling/custody, applicable water-quality/QMS evidence, batch/seal provenance, DMRV review and regulatory/product-release criteria.

## Blockchain

Only deterministic evidence-package roots are anchored. A transaction is evidence of anchoring/integrity, not proof of rainfall truth, water quality, regulatory compliance, ESG performance, or grant award.

## Institutional acceptance criteria

ES-2/ES-3 is complete when:

1. the authoritative Spanish administrative source/version is recorded;
2. every municipality is representable by an official code;
3. hierarchy relationships are deterministic;
4. municipality identity is separated from physical-site identity;
5. provider/feed bindings are pending until actual endpoints are configured and tested;
6. no environmental claim is promoted without evidence gates;
7. the registry can be refreshed without changing historical evidence identities.

## Next gate

`ES-4 — Provider/feed binding and reconciliation runtime.`
