# CA-2 — Canada Municipal / District Graph

## Objective

Turn the Illuvi Canada geography contract into an executable, versioned graph without copying a static list into the application. Statistics Canada's SGC 2021 is the canonical source. It defines four national geographic levels: geographical region, province/territory, census division and census subdivision. The hierarchy is explicitly related and covers all Canada.

Official source: https://www.statcan.gc.ca/en/subjects/standard/sgc/2021/introduction

## Implemented

1. `data/canada/sgc-2021-manifest.json` pins the source release, source URLs, expected cardinalities, province/territory mapping and node identity rules.
2. `scripts/canada-sync-sgc.mjs` downloads the two official CSV products, validates the hierarchy, hashes the inputs and produces a versioned graph snapshot.
3. `config/canada-source-registry.json` establishes source-specific claim boundaries for geography, census context and future environmental/GHG/infrastructure adapters.

Statistics Canada publishes the SGC 2021 classification structure and elements as CSV downloads, making them suitable for a reproducible ingestion pipeline.

## Canonical graph

`CA → REGION → PR/TER → CD → CSD → SITE`

The graph deliberately distinguishes a census subdivision from a physical project site. A CSD can be reportable before a Blue-Ether deployment exists.

## Node identity

- Region: `CA/R/{region_code}`
- Province/territory: `CA/PR/{PRUID}`
- Census division: `CA/CD/{CDUID}`
- Census subdivision: `CA/CSD/{CSDUID}`
- Physical project site: `CA/SITE/{CSDUID}/{SITE_ID}`

## Validation

The synchronizer checks:

- expected geographic level/cardinality;
- every CSD has a resolvable CD parent;
- every CD has a resolvable province/territory parent;
- every province/territory has a resolvable region parent;
- source SHA-256 values are preserved;
- source version is explicit;
- historical evidence is not mutated when geography changes.

## Reporting roll-up

A municipality/CSD rolls upward to its census division, province/territory, region and Canada. This supports municipal → district → provincial/territorial → regional → national reporting without changing the underlying source geography.

## Data products enabled

The graph is the address layer for:

- municipal climate baselines;
- infrastructure asset inventories;
- rainwater/water-resilience interventions;
- energy and transport activity data;
- GHG evidence packages;
- ESG indicators;
- climate-risk and adaptation projects;
- public-interest reporting;
- investment evidence rooms.

Statistics Canada census-profile products provide published contextual data at province/territory, census-division and census-subdivision levels. Annual population estimate tables provide current population context on 2021 boundaries.

## Important boundary

The graph is a geographic/reporting system. It does not itself establish legal ownership, physical installation, environmental measurement, decarbonization impact, carbon-credit issuance, regulatory certification or financial value.

## CA-2 completion condition

CA-2 is considered **READY** when the sync job has produced a valid SGC snapshot and the application consumes the generated graph through a controlled data interface rather than hard-coded geography.
