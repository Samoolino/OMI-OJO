# OMI-OJO Frontend Upgrade Blueprint

## Objective

Upgrade the frontend to expose the platform architecture without removing current project routes or evidence surfaces.

## Primary navigation

```text
Overview
Data
Evidence
Intelligence
Projects
Edge
Institutional
```

## Existing-to-new route mapping

| Existing surface | Upgrade destination |
|---|---|
| Command Center | Overview / Control Plane |
| Global Lagos | Projects / Lagos + Edge + Data |
| Harvest Intelligence | Intelligence / Water |
| Evidence & DMRV | Evidence / dMRV Control Centre |
| ESG/GHG | Intelligence / ESG + GHG |
| Investor Room | Institutional / Investor & VDR |
| country pilot pages | Projects / Global Deployments |
| dMRV portal | Evidence / dMRV Control Centre |
| QMS portal | Edge / Quality |

## Control Plane

Overview should expose system state for:

- Data health
- Evidence health
- Project health
- dMRV queues
- Release gates
- Network/anchor health
- Institutional deliverables

## dMRV Control Centre

Required views:

- Evidence Inbox
- Quality
- Reconciliation
- Calculation lineage
- Evidence Graph
- Package Builder
- Review Queue
- Verification
- Anchor Registry
- Release Gate

## Project workspace

Every project page must show:

`Overview | Requirements | Data | Sources | Methodologies | Evidence | dMRV | Reports | Milestones | Gates | Risks | Network`

## Frontend compatibility rule

Current routes remain functional during migration. New navigation can wrap/adapt existing screens before internal file movement occurs.

## Role-aware views

- Executive: system/project/institutional state.
- ESG: data, GHG, ESG, evidence and disclosure.
- Operator: nodes, telemetry, field and QMS.
- MRV/reviewer: evidence, reconciliation, calculation and verification.
- Investor/funder: projects, milestones, evidence, VDR and grant outputs.

## Visual language

The frontend should make evidence state visible: observed, forecast, modelled, satellite, calculated and proxy. Do not imply verification through styling alone.

## Implementation order

1. Shared information architecture/config.
2. Control Plane shell.
3. Project Registry surface.
4. dMRV Control Centre.
5. Data Observatory.
6. ESG/GHG and climate-risk surfaces.
7. Institutional/VDR/grant surfaces.
8. Network/verification surfaces.
9. Route cleanup only after regression validation.
