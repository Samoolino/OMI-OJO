# S6C.4 — Lagos Controlled Rain Event Watch

## Purpose
S6C.4 establishes the controlled observation window preceding any physical collection. It reconciles forecast and observation evidence, checks safety and upstream authorization, and creates an immutable event record.

## Sequence
1. Confirm S6C.1 authorization evidence is accepted.
2. Confirm S6C.2 site/GIS verification.
3. Confirm S6C.3 collector readiness.
4. Open WATCH using forecast sources.
5. Reconcile live observations when the event begins.
6. Record the event window, source identifiers, timestamps, spatial references and quality states.
7. Apply safety and fail-closed gates.
8. If all gates pass, issue a COLLECTION_WINDOW_OPEN recommendation for the separately authorized collection procedure.
9. Close the event and package evidence.

## Control rule
A forecast is never converted into an observation. A confirmed rain event is not itself permission to collect. Collection requires explicit upstream authorization and readiness.

## Evidence
The event package must contain source provenance, timestamps, event state transitions, conflicts/exceptions, operator checks and integrity digest.

## Prohibited claims
This stage cannot establish potability, Premium RainWater status, laboratory compliance, environmental-credit value, or completed physical harvest.

## Next gate
S6C.5 — First-Flush Control.
