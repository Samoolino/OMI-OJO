# S6C.11 — Lagos Blockchain Evidence Anchor Gate Runbook

## Objective
Anchor a deterministic S6C.10 DMRV package to the project's configured evidence registry while preserving an explicit boundary between evidence integrity and environmental/product truth.

## Preconditions
1. S6C.10 DMRV package is accepted for anchoring.
2. The package root/digest can be deterministically recomputed.
3. Event, site, batch and seal identities reconcile.
4. Authorized registry/network/deployment configuration is identified.
5. The submitting identity is authorized for the configured registry.
6. Replacement or corrected packages use successor references rather than mutation.

## Procedure
1. Freeze the exact DMRV package version proposed for anchoring.
2. Recompute the deterministic evidence root.
3. Compare the recomputed root with the package's recorded integrity digest.
4. Validate batch/event/site identity and package status.
5. Validate the configured chain/network and registry deployment reference.
6. Record authorized submitter identity.
7. Submit the evidence root only after all checks pass.
8. Record transaction/receipt evidence when confirmation is actually obtained.
9. Set ANCHOR_CONFIRMED only when the registry confirmation is independently traceable.
10. Preserve the anchor record and successor relationship for any later corrected package.

## Anchor semantics
The anchor establishes that a particular evidence root was submitted to a particular registry on a particular network and, when confirmed, provides an auditable transaction/receipt reference. It does **not** independently establish that the underlying measurements are true, that water is potable, that a product is premium, that regulations were satisfied, or that a GHG/environmental benefit occurred.

## Corrections
Never mutate a previously anchored evidence record. A correction creates a new deterministic package and a successor anchor referencing the prior version and the reason for correction.

## Fail-closed controls
Hold or fail for package/root mismatch, identity mismatch, unauthorized registry/network, missing deployment configuration, unauthorized submitter, ambiguous anchor identity, missing confirmation evidence when confirmation is claimed, or missing integrity evidence.

## Next gate
**S6C.12 — Premium Condition Review**

Physical/product status remains **NOT_RELEASED**.
