# Frontend Production Control Surface

The frontend is an operational presentation layer for the production framework. It must expose the current gate, scope, evidence semantics and next controlled procedure without creating evidence that does not exist.

## Current surface

**Current gate:** S8.1 — Site Onboarding and Local Authorization  
**Next gate:** S8.2 — Site Operational Readiness and Controlled Pilot  
**Physical status:** NOT_RELEASED

## Production sequence exposed to users

M-1 → S6A → S6B → S6C → POST-S6C → S7 → S8 → S8.1

Each stage is a control boundary. A frontend badge such as IMPLEMENTED means the software/control definition exists; it does not mean the corresponding physical or empirical activity occurred.

## Scope surface

The landing navigation exposes:
- Project Scope
- Production Control
- Global Lagos
- Harvest Intelligence
- Evidence & DMRV
- ESG / GHG
- Investor Room

## Mandatory semantic boundaries

The interface must visibly preserve:
- administrative node ≠ physical field site;
- forecast ≠ observed measurement;
- modelled/satellite evidence ≠ direct observation;
- blockchain anchor ≠ environmental truth;
- software readiness ≠ regulatory/product release;
- reporting grid ≠ completed harvest operation.

## S8.1 frontend procedure

The Production Control view presents:
1. Define site.
2. Verify identity.
3. Authorize.
4. Operationalize.
5. Admit.
6. Advance to S8.2 only when controls pass.

The UI must remain fail-closed and must not display site onboarding as evidence of harvest, laboratory results, batch creation or product release.

## Relationship to authoritative records

The frontend is subordinate to the production manifest and evidence packages. When future live adapters are connected, the displayed status must be derived from authoritative records rather than inferred from UI interaction.

## Investor/public interpretation

The interface is intended to make the institutional workflow inspectable: project scope → production gate → evidence class → verification state → release boundary. It is not itself a verification authority.
