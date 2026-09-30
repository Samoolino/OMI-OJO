# Anchor Verification Flow

The network integration is intentionally chain-neutral.

```text
Released Snapshot
      ↓
Evidence Package
      ↓
Deterministic Root Hash
      ↓
IntegrityAnchorService
      ↓
Network Adapter
      ↓
Anchor Registry
      ↓
Public Verification
```

## Verification states

- `MATCHED`: stored anchor root equals the expected evidence root.
- `MISMATCHED`: an anchor exists but the expected root differs.
- `NOT_FOUND`: no anchor is registered for the requested identifier.

## Boundary

An anchor proves correspondence to a deterministic evidence/reporting state. It does not certify environmental truth, measurement accuracy, carbon credit validity, ESG performance, or investment suitability.

The production adapter must be supplied only after network authorization, contract deployment, security review, and testnet acceptance. The repository currently includes an in-memory adapter for deterministic integration testing only.
