# Integration Implementation Plan

## Objective

Integrate the existing climate/ESG reporting runtime with governed release, grant work packages, and a chain-agnostic network integrity layer without changing environmental evidence semantics.

## Current production spine

DISCOVER → PLAN → GATE → EXECUTE → NORMALIZE → QC → EVIDENCE PACKAGE → REPORTABILITY → DRAFT SNAPSHOT → PERSISTENCE

## Integrated target

SOURCE GIT → ORCHESTRATION → EVIDENCE → dMRV/CLAIM → REVIEW/RELEASE → REPORTING/VDR/GRANTS → NETWORK INTEGRITY → PUBLIC VERIFICATION

## Implementation sequence

1. **Source Git governance** — canonical configuration schemas, revisions and reproducibility metadata.
2. **Release governance** — immutable DRAFT/REVIEW/APPROVED/RELEASED state machine with exception states.
3. **Claim/evidence graph** — trace every material reporting/VDR claim to source, methodology, observation, QC and release.
4. **Grant work-package engine** — map funded capabilities to milestones, acceptance criteria, tests and evidence.
5. **Network registry** — chain/environment definitions with controlled lifecycle.
6. **Anchor adapter** — chain-neutral interface for deterministic evidence/snapshot roots.
7. **Anchor registry and verification** — retain transaction/proof metadata and independently verify roots.
8. **VDR read model** — expose accepted evidence and claims without creating a second evidence truth.

## Grant/network boundary

Grant funding pays for measurable work packages and their acceptance evidence. Blockchain/network infrastructure provides integrity, timestamping and verification of deterministic roots. Neither funding nor blockchain changes environmental truth.

## Network boundary

Raw environmental observations, PII and VDR documents remain off-chain. Only deterministic integrity commitments and non-sensitive references are eligible for anchoring.

## Definition of done for the integration

- every released snapshot is linked to an evidence package;
- every release records configuration and policy revisions;
- every grant work package has machine-readable acceptance scope;
- network definitions are versioned and environment-gated;
- anchor adapters are replaceable;
- a public verifier can reproduce/compare the anchored root;
- VDR and grant outputs consume the same governed evidence state.
