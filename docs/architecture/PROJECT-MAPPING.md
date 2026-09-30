# OMI-OJO Project Mapping — UB-02

This registry deliberately preserves historical project identifiers.

| Project | Strategic role | Product injection | Climate/ESG layer | Primary evidence |
|---|---|---|---|---|
| M-1 | Platform baseline | All products | L0-L7 | production manifests |
| P1-P20 | Core capability programme | Data/Evidence/Intelligence/Institutional as applicable | L1-L7 | production gates |
| S4 | Controlled evidence integration | Data + Evidence | L1-L6 | provider/observation/evidence contracts |
| S5 | Global deployment framework | Data + Intelligence + Institutional | L1-L7 | country/project contracts |
| S6A | Network/integrity infrastructure | Evidence + Network | L6-L7 | deterministic package + anchor contract |
| S6B | Builder/grant infrastructure | All platform infrastructure | L1-L7 | work packages + acceptance evidence |
| S6C | Lagos physical validation | Edge + Water + Data + dMRV | L0-L7 | authorization, rain event, custody, QMS, dMRV |
| S6C.2 | Survey/GIS cross-check | Edge + Data | L0-L3 | coordinate/venue verification |
| ES4/ES5/ES6 | Illovediza-Fuerza evidence sequence | Data + Evidence | L1-L6 | reconciliation + dMRV package |
| Global Lagos | Reference/proof deployment | Data + Evidence + Intelligence | L0-L7 | 40-node grid, source/indicator registry |
| Lagos-to-Dubai | Global deployment programme | Data + Intelligence + Institutional | L1-L7 | country pilot contracts |

## P1-P20 rule

The production manifest remains authoritative for P1-P20 gate status. UB-02 does not invent individual project descriptions where the repository does not expose a stable public title. Each P-series item should receive a `platform_capability` and `product_injection` mapping in the Project Registry before implementation work is moved.

## Geographic mapping

- Nigeria/Lagos = reference/proof pilot.
- Portugal, Chile, Mexico, UAE = international deployment surfaces using the common evidence semantics.
- Brazil = anchor-pending boundary until the repository gate changes.
- International deployments must not inherit unsupported evidence values from Lagos.

## Project injection contract

Every project declares:

```yaml
project_id:
vertical:
geography:
products:
data_requirements:
sources:
methodologies:
indicators:
evidence_requirements:
reports:
network:
anchor:
release_gates:
```

## Required project lifecycle

`PROJECT -> REQUIREMENTS -> SOURCES -> METHODOLOGIES -> INGESTION -> QC -> RECONCILIATION -> dMRV -> EVIDENCE -> CLAIM -> REPORT -> ACCEPTANCE -> OPTIONAL ANCHOR`
