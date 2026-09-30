# POST-S6C — Lagos Release Authorization and Public Verification Runbook

## Objective
Provide the final controlled boundary between a completed evidence chain and any actual product release or public verification statement.

## Preconditions
1. S6C.12 premium-condition review is complete.
2. Applicable regulatory/product authorization has been independently documented.
3. Batch and seal identity reconcile to the reviewed evidence package.
4. DMRV package and required blockchain anchor references reconcile.
5. Release authority, scope and effective time are explicit.
6. Public-facing claims have evidence references and pass privacy/redaction review.
7. Rollback/hold/recall conditions are defined.

## Procedure
1. Create a unique release-review ID.
2. Freeze the exact batch, DMRV package, premium review and anchor references.
3. Verify the applicable authority and its scope.
4. Record any required independent review.
5. Define the precise release scope: batch, quantity if measured, site, effective period and permitted claims.
6. Record the release decision and authority.
7. Run the public-verification preparation review.
8. Expose only public-safe evidence references and claims.
9. Record a public verification reference when the verification surface is actually available.
10. Mark RELEASED only after all required release conditions are satisfied.

## Release semantics

### RELEASE_REVIEW_READY
Evidence is assembled for the final authorization decision.

### AUTHORIZED_RELEASE
The competent release authority has recorded an affirmative decision for the specified scope.

### PUBLIC_VERIFICATION_READY
The authorized release can be represented through a public-safe verification surface.

### RELEASED
Physical/product release has actually occurred under the recorded authority and scope.

### HOLD / REJECTED
Any material unresolved control prevents release.

## Fail-closed requirements
No release is inferred from software readiness, DMRV completeness, blockchain anchoring, investor readiness, grant readiness or premium review alone.

## Public verification
The public surface must distinguish:
- what was measured;
- what was calculated;
- what was modelled or forecast;
- what was verified;
- what was anchored;
- what was authorized for release.

Sensitive operational or personal information must not be published merely because it exists in the evidence package.

## Rollback
A post-release material discrepancy must trigger the documented hold/recall/rollback process and, where the evidence package changes, a successor package and anchor rather than mutation of historical evidence.

## Next gate
**S7 — Post-Release Monitoring and Audit**

Until actual authorization and empirical release records exist, physical/product status remains **NOT_RELEASED**.
