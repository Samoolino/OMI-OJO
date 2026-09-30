# S6C.5 — Lagos Controlled First-Flush Control Runbook

## Objective
Execute a fail-closed first-flush diversion control between a qualified rain event and controlled collection. The gate establishes that the initial runoff has been diverted according to an approved method and that the system is eligible to enter controlled collection.

## Scope
This gate covers the physical control action, instrumentation/provenance, operator record and evidence integrity. It does not certify water quality, authorize product release or create a premium-water claim.

## Preconditions
1. S6C.4 rain-event watch is accepted for the same site/event.
2. Field/site authorization remains valid.
3. Collector readiness is accepted.
4. First-flush hardware is identified and configured.
5. A documented threshold method is approved for the controlled test.
6. Operator identity, communications and safety checks are recorded.
7. Time sources are synchronized.

## Procedure
1. Create the S6C.5 control record and bind it to the S6C.4 event ID.
2. Verify site, collector and first-flush device identity.
3. Record the threshold method, revision, value and unit before diversion begins.
4. Place the system in diversion mode and record DIVERSION_ACTIVE with timestamp.
5. Observe the diversion until the approved threshold is reached.
6. Record metered volume and/or duration plus instrument and calibration references where applicable.
7. Record the diversion completion timestamp and enter DIVERSION_COMPLETE.
8. Review safety, provenance, equipment and contamination checks.
9. If all controls pass, record COLLECTION_ELIGIBLE; otherwise enter HOLD or FAILED.
10. Preserve the evidence record and integrity digest before the next gate.

## Evidence package
The package must contain the upstream event reference, device/configuration identity, approved threshold method, timestamps, diversion volume or duration, instrument/calibration references, operator action log, site identity and integrity digest.

## Fail-closed controls
Do not progress if authorization is missing/expired, the event and site do not match, the first-flush system is unavailable or misconfigured, the threshold is undefined/unapproved, instrumentation or timing fails, operator identity is unavailable, contamination is suspected, field conditions are unsafe, or provenance/integrity evidence is incomplete.

## Gate interpretation
COLLECTION_ELIGIBLE means the first-flush control has passed and the system may enter S6C.6. It does not mean that water was successfully collected, that water quality is acceptable, that a batch exists, or that any premium/regulatory claim is established.

## Next gate
**S6C.6 — Controlled Collection and Sample Capture**

Actual field execution remains NOT_RELEASED until the required empirical evidence is recorded and independently reviewed.
