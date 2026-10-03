# Illuvi Canada — National Decarbonization & Data Assetification Project

## 1. Project intent

Illuvi Canada is the Canada implementation of the Blue-Ether geographic evidence strategy: map the country, structure its municipalities from authoritative district/census-divisional relationships, and use the same DMRV/evidence infrastructure to develop decarbonization and climate-resilience products.

Canada should **not** be forced into a foreign administrative model. Statistics Canada's Standard Geographical Classification (SGC) provides the canonical reporting hierarchy: geographical region → province/territory → census division → census subdivision. The project can expose friendly report labels such as “state” or “district”, but the canonical record must retain the official type and code.

## 2. National reporting hierarchy

`CANADA → REGION → PROVINCE/TERRITORY → DISTRICT (CENSUS DIVISION) → MUNICIPALITY/CSD → SITE → INDICATOR → EVIDENCE`

The six SGC regions are Atlantic, Quebec, Ontario, Prairies, British Columbia and Territories. SGC 2021 defines 13 provinces/territories, 293 census divisions and 5,161 census subdivisions. Census divisions can correspond to counties, regional municipalities, regional districts or equivalent statistical areas; census subdivisions are the general statistical term for municipalities or municipal equivalents.

### Reporting semantics

| Project label | Canonical Canadian layer | Purpose |
|---|---|---|
| Nation | Canada | National roll-up |
| Region | SGC geographical region | Cross-provincial reporting |
| State | Province or territory | Presentation alias only |
| District | Census division | Regional/municipal aggregation |
| Municipality | Census subdivision | Local reporting unit |
| Site | Qualified physical/project location | Measurement and intervention boundary |

## 3. Mapping the Nation

The national map is a **reporting index first** and a physical deployment map second.

1. Import the selected SGC release and preserve its version.
2. Register all 13 province/territory codes.
3. Register the six regions.
4. Register all census divisions and their parent relationships.
5. Register all census subdivisions and their parent relationships.
6. Attach boundary references and stable geographic identifiers.
7. Create representative nodes without implying physical installations.
8. Promote a node to measured/project status only after a source or field deployment exists.

The resulting graph supports both top-down reporting and bottom-up evidence: municipality → district → province/territory → region → Canada.

## 4. Municipalities from districts

A district is an aggregation/reporting object. A municipality/CSD is a lower-level object.

Each municipal record should carry:

- canonical SGC code;
- canonical name and type;
- parent census division;
- parent province/territory;
- parent SGC region;
- boundary/version reference;
- reporting status;
- site/project references;
- evidence package references.

This prevents a dashboard label from being mistaken for a physical asset, legal boundary or measurement.

## 5. Product development on decarbonization

The infrastructure becomes a product-development system rather than only a dashboard.

### Product A — Municipal Decarbonization Evidence Package

Municipality baseline → activity data → boundary → emission-factor method → intervention → measured change → QA/reconciliation → DMRV evidence package → report.

### Product B — Infrastructure Climate Asset Record

Asset identity → location → owner/operator boundary → condition data → climate exposure → intervention → resilience metric → lifecycle evidence → verification.

### Product C — Water & Rain Resilience Package

Rainfall/atmospheric conditions → collection opportunity → water-system intervention → measured volume/quality where applicable → GHG/energy implications → evidence package.

### Product D — Regional GHG Evidence Ledger

Activity data → factor source/version → calculation → uncertainty/quality metadata → reconciliation → period-close evidence → reportable GHG record.

### Product E — Climate Investment Evidence Room

Project boundary → baseline → risks → intervention → capex/opex evidence → expected/observed indicators → safeguards → evidence index → investor/public disclosure boundary.

These are evidence products. They do not automatically constitute carbon credits, securities, regulatory certifications or ownership rights.

## 6. Assetification model

Assetification means making useful evidence **addressable, versioned, reproducible and auditable**.

### Data assets

- geography assets;
- observation assets;
- infrastructure assets;
- activity-data assets;
- GHG calculation assets;
- ESG evidence assets;
- project evidence assets.

### Framework relics

A framework relic is an immutable/versioned reference artifact such as:

- geography release;
- methodology;
- emission-factor version;
- boundary rule;
- indicator definition;
- schema;
- reconciliation rule;
- source mapping;
- verification rule.

Each relic receives an identifier, version, effective date, supersession state, provenance and content hash.

## 7. Evidence chain

`SOURCE → OBSERVATION → QUALITY → RECONCILIATION → EVIDENCE PACKAGE → HASH → ANCHOR → REPORT`

Blockchain remains an integrity/verification layer. It does not create environmental truth and does not replace the authoritative source or methodology.

## 8. Canada implementation phases

### CA-0 — Strategy and boundary
Freeze project purpose, geography version, source policy, asset classes and claim boundaries.

### CA-1 — National map
Load Canada → region → province/territory → census division → census subdivision.

### CA-2 — Municipal graph
Generate parent-child municipality/district relationships and reporting APIs.

### CA-3 — Evidence registry
Register environmental, infrastructure, GHG and ESG source adapters.

### CA-4 — Decarbonization product pilots
Select representative municipalities/districts for measured intervention packages.

### CA-5 — Assetification
Hash/version reusable evidence packages and framework relics.

### CA-6 — DMRV and verification
Reconcile evidence, create canonical packages and anchor evidence roots.

### CA-7 — Scale
Expand from representative nodes to qualified municipal and physical project sites.

## 9. Governance boundary

The geographic layer is not a substitute for legal jurisdiction. Indigenous governance, municipal authority, provincial/territorial legislation, federal programmes, privacy obligations and source-specific licensing must remain explicit in each project boundary.

## 10. Production definition

`REPORTABLE → MEASURED → VALIDATED → VERIFIED → ANCHORED`

A geographic node may be reportable before measurement. A measurement may exist without being validated. A validated package may remain unanchored. These states must never be collapsed into one claim.

## 11. Relationship to the wider Blue-Ether network

Canada inherits the same core infrastructure as Lagos and other international pilots:

- canonical source registry;
- geographic node model;
- environmental evidence schema;
- GHG/ESG reporting;
- non-contradiction engine;
- DMRV;
- hash-based evidence roots;
- optional blockchain anchoring;
- VDR evidence index;
- analytics/mapping surfaces.

Only the geographic hierarchy, source adapters, jurisdictional controls and product deployment boundaries change.
