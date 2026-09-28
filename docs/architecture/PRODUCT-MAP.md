# OMI-OJO Product Map

## Product architecture

| Product | Technical role | Primary users | Core outputs |
|---|---|---|---|
| Data | Source and governed-data layer | data/ESG teams, operators | observations, datasets, source lineage |
| Evidence | dMRV and assurance layer | MRV, auditors, reviewers | evidence packages, claims, verification |
| Intelligence | interpretation layer | climate/water/ESG teams | indicators, risk, GHG, insights |
| Institutional | delivery layer | funders, investors, regulators | VDR, reports, grant evidence, audit packs |
| Edge | physical layer | field/operators | telemetry, field observations, custody |
| Premium | controlled product-release layer | product/institutional teams | premium evidence packages and release decisions |

## Legacy-to-upgrade mapping

| Existing product | UB-02 role |
|---|---|
| OMI-OJO OS | Core platform/control plane |
| OMI-OJO Nodes | Edge |
| OMI-OJO Intelligence | Intelligence |
| OMI-OJO MRV | Evidence/dMRV |
| OMI-OJO Institutional | Institutional |
| OMI-OJO Premium | Premium evidence/release |

## Technical modules

```text
Source Registry
  -> Ingestion / adapters
  -> Observation schema
  -> Normalization
  -> Quality
  -> Reconciliation
  -> Calculation / methodology
  -> Evidence Graph
  -> dMRV package builder
  -> Review / verification
  -> Anchor adapter
  -> Report / VDR / disclosure
```

## Required shared registries

- Project Registry
- Source Registry
- Methodology Registry
- Indicator Registry
- Claims Registry
- Evidence Registry
- Network Registry
- Anchor Registry
- Report Registry
- Grant/Work Package Registry

## Product boundaries

Data is responsible for **what was observed and where it came from**.

Evidence is responsible for **whether the observation/calculation can support a defined claim**.

Intelligence is responsible for **derived indicators, interpretation and risk analysis**.

Institutional is responsible for **audience-specific delivery and controlled disclosure**.

Blockchain is an **integrity service**, not a truth oracle.
