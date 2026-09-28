# OMI-OJO Report Architecture

## One evidence truth, many controlled views

Reports must be generated from the same accepted evidence package. Audience-specific reports change presentation and permissible detail, not the underlying evidence truth.

## Common report envelope

```text
Report ID
Project / Site / Period
Scope and boundary
Data sources
Methodologies and versions
Indicators / calculations
Evidence references
Quality / reconciliation state
Review / verification state
Claims and limitations
Integrity / anchor reference
Release authority
Release state
```

## Report families

### Public
Project status, key indicators, methodology summary, evidence links, limitations, verification/anchor reference.

### Grant / funder
Work package, milestone, activities, outputs, acceptance evidence, budget status, variance, next gate.

### ESG
Metric, boundary, period, source, activity data, methodology, calculation, assumptions, uncertainty, evidence and review status.

### GHG
Scope, activity data, factor source/version, method, calculation, uncertainty, evidence and review.

### Investor / VDR
Project, technology, data, evidence, IP, methodology, risks, funding, milestones, validation, security and financial materials.

### Regulatory
Jurisdiction-specific schema and evidence requirements.

### Audit
Full lineage from claim to source, observation, calculation, review, verification and anchor.

## Report generation rule

`Accepted Evidence Package -> Report Template -> Audience Filter -> Claim Policy -> Release Gate`

No report may imply a stronger evidence state than the underlying package supports.
