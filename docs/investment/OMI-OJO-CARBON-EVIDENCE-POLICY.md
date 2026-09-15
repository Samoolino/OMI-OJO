# OMI-OJO — Carbon-Relevant Evidence & Credit Eligibility Policy

## Purpose

Define how OMI-OJO can support future carbon/environmental-credit projects while preventing unsupported claims.

## 1. Controlled terminology

- **Carbon-relevant data:** activity or environmental data that may feed an applicable emissions methodology.
- **Conceptual carbon claim:** a hypothesis that an intervention could generate measurable emission benefits; not a credit.
- **Calculated reduction:** a methodology-based calculation with documented inputs and assumptions; not yet verified/issued.
- **Validated project:** an authorized validation process has accepted the project design under an applicable standard/methodology.
- **Verified reduction:** an authorized verification process has accepted monitored results.
- **Issued credit:** a recognized registry/standard has issued units under its rules.
- **Retired credit:** an issued unit has been retired and is no longer available for transfer.

## 2. Evidence state machine

```text
CONCEPT
  ↓
ACTIVITY DATA
  ↓
METHODOLOGY ELIGIBILITY
  ↓
BASELINE + ADDITIONALITY
  ↓
MONITORING PLAN
  ↓
CALCULATED IMPACT
  ↓
VALIDATION
  ↓
MONITORING
  ↓
VERIFICATION
  ↓
ISSUANCE
  ↓
RETIREMENT
```

No state may be skipped in external claims.

## 3. Minimum evidence package

For each carbon-relevant project, maintain:

1. project identifier and boundary;
2. activity description;
3. geographic reference;
4. baseline definition;
5. additionality rationale;
6. monitoring variables;
7. measurement instruments/data sources;
8. methodology and version;
9. emission factors and source;
10. calculation version;
11. uncertainty treatment;
12. leakage/reversal treatment where applicable;
13. double-counting controls;
14. raw evidence references;
15. evidence hashes;
16. reviewer identity and decision;
17. registry/standard reference where applicable;
18. issuance/retirement evidence if units exist.

## 4. Water-project boundary

Rainwater capture, storage or reuse does **not automatically create carbon credits**. Potential climate benefits must be tied to an eligible methodology and a defensible counterfactual, such as an evidenced displacement of an emissions-intensive water supply or treatment activity.

OMI-OJO therefore records water activity first and treats any carbon conversion as a separate methodology layer.

## 5. Blockchain boundary

Blockchain is used to anchor deterministic evidence-package hashes and provide auditability. It does not certify additionality, validate emission factors, verify physical activity or issue carbon credits.

## 6. Investor language

Approved:

> “OMI-OJO is building carbon-relevant activity-data and dMRV infrastructure that can support eligible environmental-credit projects subject to methodology, validation, verification and registry requirements.”

Not approved:

> “OMI-OJO already generates certified carbon credits.”

unless independently documented issuance evidence exists.

## 7. Gate ownership

- Technical/Data Lead: measurement and provenance.
- ESG/GHG Lead: methodology and calculations.
- Independent Reviewer: validation/verification acceptance.
- Legal/Regulatory Lead: claims and market eligibility.
- Governance: release of external claims.

## 8. Reporting rule

Every investor/funder report must state whether an environmental number is:

`OBSERVED | FORECAST | MODELLED | CALCULATED | VALIDATED | VERIFIED | ISSUED | RETIRED`

and must not collapse these states into “impact achieved.”
