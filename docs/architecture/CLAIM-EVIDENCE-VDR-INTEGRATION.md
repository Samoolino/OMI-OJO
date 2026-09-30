# Claim → Evidence → VDR Integration

The reporting system now has a canonical traceability boundary for institutional claims.

```text
CLAIM
  ↓
INDICATOR
  ↓
OBSERVATION(S)
  ↓
SOURCE + METHODOLOGY
  ↓
EVIDENCE PACKAGE
  ↓
REPORTING SNAPSHOT
  ↓
REVIEW / RELEASE
  ↓
VDR / GRANT EVIDENCE
  ↓
OPTIONAL NETWORK ANCHOR
```

## Rules

- A claim references an immutable evidence package and reporting snapshot.
- Evidence class is not promoted by claim creation or release.
- VDR artifacts consume governed claims; they do not create environmental truth.
- A blockchain anchor proves integrity of a referenced root; it does not independently verify the environmental observation.
- Grant acceptance should reference implementation commits, tests, evidence packages and release decisions.

## Builder / S6B mapping

The S6B work package remains the controlled implementation target: deterministic dMRV package builder, blockchain evidence anchor, public verification, security/governance, and VDR evidence package. Funding status remains separate from implementation status and must never be represented as awarded without documentary evidence.
