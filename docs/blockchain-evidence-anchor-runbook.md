# S6A — Blockchain Evidence Anchor Runbook

## Purpose

Provide a minimal, auditable blockchain layer for OMI-OJO DMRV evidence packages. The blockchain stores only an evidence package identifier and deterministic digest plus transaction metadata.

## On-chain boundary

The chain does **not** store or certify:

- rainfall truth;
- water quality;
- potability;
- GHG reductions;
- ESG compliance;
- regulatory approval;
- grant eligibility;
- investor returns.

It provides tamper-evidence for the referenced package.

## Lifecycle

`PACKAGE_READY -> HASHED -> ANCHOR_SUBMITTED -> ANCHORED -> PUBLICLY_VERIFIABLE`

Failures remain `ANCHOR_FAILED` and never become verified by UI presentation.

## Contract

`contracts/EvidenceAnchorRegistry.sol`

The registry accepts:

- `packageId` — deterministic identifier for the evidence package;
- `digest` — bytes32 digest of the canonical evidence package.

It rejects empty identifiers and duplicate package IDs. `verify(packageId, digest)` provides a deterministic on-chain equality check.

## Deployment controls

Before any production deployment:

1. compile with the pinned Solidity toolchain;
2. run unit tests for first anchor, duplicate anchor, empty values and verification;
3. deploy to a supported test network;
4. record chain ID, contract address, compiler/toolchain version and deployment transaction;
5. verify source code where supported;
6. run an end-to-end package -> hash -> transaction -> readback test;
7. preserve transaction receipts in the VDR;
8. conduct security review before production funds or production evidence are used.

## Network strategy

The application remains chain-agnostic. A first controlled deployment should use one supported EVM network. A second network can be added only after the first complete lifecycle passes and there is a documented redundancy/interoperability reason.

## Institutional evidence

The VDR must retain the original package, canonical serialization, digest, package schema version, chain ID, contract address, transaction hash, block timestamp, submitter identity and verification result.

## Token boundary

No project token is required for S6A. Native network gas/test tokens are infrastructure resources only. Any future project token requires a separate legal, regulatory, accounting and governance workstream.

## Acceptance gate

S6A passes when a controlled test package can be deterministically hashed, anchored, retrieved and verified from the deployed contract, with the transaction evidence retained outside the chain.

## Next gate

`S6B — Grant/Builder Infrastructure Evidence Package and controlled funding applications.`
