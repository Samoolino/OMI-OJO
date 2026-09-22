# S6A — Blockchain Evidence Anchor Production Specification

## Purpose

S6A validates OMI-OJO as an evidence infrastructure system before any physical Premium RainWater production claim.

The acceptance chain is:

```
Evidence Records
  → Canonical Evidence Package
  → Deterministic Evidence Root
  → Authorized Anchor Submission
  → Blockchain Transaction
  → Anchor Receipt
  → Independent Verification
```

S6A does not establish water quality, environmental truth, regulatory compliance or commercial product status.

## Scope

S6A covers:

1. deterministic evidence-package construction;
2. canonical hashing;
3. network/contract registry;
4. authorized anchor submission;
5. transaction receipt capture;
6. public verification;
7. append-only correction handling;
8. security and release evidence;
9. builder/grant evidence packaging.

S6A does not include project-token issuance.

## Evidence package

Every anchorable package must contain, at minimum:

| Field | Requirement |
|---|---|
| evidence_id | Stable unique identifier |
| schema_version | Immutable package schema version |
| project_id | OMI-OJO project identifier |
| evidence_class | OBSERVED / FORECAST / MODELLED / SATELLITE / CALCULATED / PROXY |
| source_refs | Source/provider identifiers |
| observation_refs | Referenced observations |
| event/site_refs | Applicable event/site identifiers |
| methodology_ref | Method/version used |
| quality_state | Quality decision |
| created_at | Package creation timestamp |
| observation_window | Relevant time window |
| geography_ref | Non-sensitive geographic reference |
| content_hashes | Hashes of referenced canonical content |
| parent_evidence | Optional predecessor/successor linkage |
| status | Controlled lifecycle state |

Security-sensitive coordinates, credentials and personally identifiable information must not be placed on-chain.

## Canonicalization rule

The package must be serialized deterministically before hashing.

Required controls:

- UTF-8 encoding;
- stable field names;
- deterministic key ordering;
- normalized numeric representation;
- normalized timestamps;
- explicit schema version;
- no transient UI fields;
- no random identifiers generated during hashing;
- no secrets;
- no mutable external content embedded without its own hash.

The same package must produce the same root independent of client or deployment.

## Root calculation

Initial implementation:

```text
canonical_package
      ↓
SHA-256
      ↓
evidence_root
```

Where multiple evidence objects form a package, a deterministic Merkle-style root may subsequently be introduced. The root algorithm and version must always be recorded.

## Anchor record

The off-chain verification registry records:

```text
evidence_id
schema_version
evidence_root
network_id
chain_id
contract_address
transaction_hash
block_number
block_timestamp
anchor_status
anchored_at
verifier_version
```

The blockchain record should contain only the minimum information required to prove integrity and locate the anchor.

## Network registry

Each supported network is represented by:

- network identifier;
- chain ID;
- environment;
- RPC/provider reference;
- explorer reference;
- anchor contract address;
- contract version;
- deployment transaction;
- finality policy;
- cost policy;
- authorized submitter policy;
- status.

Initial status vocabulary:

```
CANDIDATE
CONTROLLED_TEST
VALIDATED
PRODUCTION_ANCHOR
HOLD
DEPRECATED
```

One network is validated first. Multi-network redundancy is a later milestone.

## Anchor authorization

Anchor submission must be explicitly authorized.

The system must reject:

- unknown evidence IDs;
- malformed roots;
- duplicate unauthorized anchors;
- unsupported schema versions;
- unknown network/contract versions;
- unauthorized submitters;
- packages containing prohibited secrets;
- superseded evidence submitted as a new primary record without successor linkage.

## Verification

A verifier must independently reconstruct or retrieve:

1. evidence package;
2. canonicalization version;
3. evidence root;
4. blockchain anchor;
5. transaction receipt;
6. network/contract identity.

Verification result:

```
MATCHED
MISMATCHED
NOT_FOUND
SUPERSEDED
HOLD
```

A MATCHED result means the supplied package corresponds to the anchored root. It does not mean that the underlying environmental or physical claim is independently true.

## Correction policy

Evidence is append-only.

If an error is discovered:

```
Original Evidence
      ↓
CORRECTION / SUCCESSOR RECORD
      ↓
New Evidence Root
      ↓
New Anchor
```

The original anchor remains discoverable and is never silently overwritten.

## S6A acceptance gates

### S6A.1 — Package determinism
Two independent executions produce the same root for identical canonical content.

### S6A.2 — Anchor contract
Controlled network deployment accepts valid evidence roots and rejects invalid/unauthorized submissions.

### S6A.3 — Receipt reconstruction
Transaction, block and contract identity can be reconstructed from the anchor record.

### S6A.4 — Public verifier
A public-safe verifier returns the correct integrity status without exposing restricted data.

### S6A.5 — Correction handling
A corrected record creates a successor evidence chain without mutating historical evidence.

### S6A.6 — Security review
Secrets, privileged actions, replay/duplicate submissions and malformed inputs are tested.

### S6A.7 — Builder/grant evidence
The complete lifecycle is packaged as a reproducible infrastructure demonstration.

## S6A release criterion

S6A becomes `VALIDATED` only when:

```
DETERMINISTIC PACKAGE
+ CONTROLLED ANCHOR
+ RECEIPT RECONSTRUCTION
+ PUBLIC VERIFICATION
+ CORRECTION TEST
+ SECURITY REVIEW
```

are all evidenced.

S6A does not promote S6B physical production.

## Relationship to S6B

S6B remains separately gated:

```
S6A — Digital evidence infrastructure
                ↓
S6B — Authorized physical validation
                ↓
Premium-condition decision
                ↓
Regulatory/product release
```

A successful blockchain anchor cannot substitute for water/QMS, field, regulatory or independent DMRV evidence.

## Funding evidence

S6A funding requests should describe measurable infrastructure:

- evidence-package builder;
- anchor contract;
- network deployment;
- verifier;
- security review;
- monitoring;
- documentation;
- test evidence.

Builder/testnet/gas resources remain infrastructure resources. Project-token issuance remains `DEFERRED`.
