# Global Lagos — Video Evidence + DMRV Procedure

## Purpose

This procedure defines how future authorized live harvest and post-collection video feeds become cryptographically linked evidence inside Blue-Ether OS. The current Global Lagos phase remains reporting-only: no physical harvest, bottling, production or live operational claim is made until field validation gates pass.

## 1. Video feed port

The DMRV backend exposes a media-ingestion boundary rather than assuming one streaming protocol:

- **WebRTC** — low-latency browser/operator live viewing where supported.
- **SRT** — resilient contribution feed for field cameras/mobile encoders.
- **RTSP bridge** — controlled ingestion from compatible IP cameras; RTSP is not exposed directly as a public browser feed.
- **HTTPS metadata API** — feed health, segment manifests and evidence metadata.
- **Object storage archive** — immutable evidence media/segments and manifests.

The frontend may show `LIVE`, `RECORDING`, `ARCHIVED`, `DEGRADED`, or `OFFLINE`, but must never infer that a live stream means a verified harvest.

## 2. Operational video classes

Each authorized field operation receives an `operation_id` and one or more camera/feed records:

1. rainfall onset / site condition
2. collection setup and collector state
3. first-flush diversion
4. collection commencement
5. collection completion
6. container/batch transfer
7. sampling and water-quality custody
8. treatment/bottling where authorized
9. sealing and batch identification
10. storage/custody handoff
11. incident or exception recording

## 3. Cryptographic evidence procedure

For each media segment:

`capture → timestamp → metadata canonicalization → SHA-256 segment hash → previous-hash link → signed manifest → evidence-root construction → DMRV package`

The manifest records camera/device identity, venue, operation, timestamps, device-clock status, location status, capture profile, segment hashes and linked operational event IDs. A private signing key is never stored in the repository; only a key reference and resulting signature may be recorded.

A sequence of segment hashes forms a tamper-evident chain. A deterministic manifest is hashed and incorporated into a hash-tree/evidence root. The root can later be anchored to a supported blockchain without treating the blockchain transaction itself as proof of the underlying physical event.

## 4. DMRV linkage

Video is one evidence modality. Verification requires reconciliation against available independent evidence:

`Video → Rain Event → Telemetry → Collection Record → First Flush → Sample/Custody → QMS/Lab → Batch → Seal → Evidence Root → DMRV Review → Anchor`

A video-only record cannot promote `MODELLED`, `FORECAST`, `UNVERIFIED` or other records to `OBSERVED` or `VERIFIED`.

## 5. Integrity and failure states

- Missing timestamp: `REVIEW_REQUIRED`
- Missing venue/operation identity: `REVIEW_REQUIRED`
- Broken hash chain: `REJECTED` pending investigation
- Missing media segment: `REVIEW_REQUIRED`
- Clock drift outside configured tolerance: `REVIEW_REQUIRED`
- Unauthenticated device: `UNVERIFIED`
- Coordinate unavailable: evidence may remain usable but location status must be explicit
- Conflicting independent evidence: `REVIEW_REQUIRED`
- Correction: append successor record; never overwrite original evidence

## 6. Public/investor views

Public viewers receive only sanitized feed status and approved evidence metadata. Restricted operational video requires authorization. Investor evidence views can expose provenance, hashes, event linkage, reconciliation status and review state without exposing credentials or security-sensitive locations.

Governor's Residence remains generalized and security-controlled; no exact operational camera location or public live feed is permitted without explicit authorization.

## 7. Production gate

Video integration is a production evidence capability only after controlled tests demonstrate capture, segmentation, hashing, manifest reconstruction, chain verification, clock handling, event linkage, access control, retention and DMRV reconciliation. Until then, the UI must remain `VIDEO EVIDENCE · GATED`.
