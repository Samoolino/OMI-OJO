# Global Lagos Coordinate Verification

## Purpose

Establish a controlled geotag workflow for the 40-node Global Lagos reporting grid without inventing coordinates.

## Status model

`REFERENCE_ONLY → SURVEY_REQUESTED → SURVEY_CAPTURED → GIS_CROSSCHECKED → VERIFIED`

A node remains `PENDING_SURVEY` when its exact site coordinate has not been obtained from an authorized survey or authoritative GIS record.

## Required evidence

Every verified coordinate record must contain:

- `venue_id`
- latitude / longitude in WGS84
- `accuracy_m`
- coordinate precision class (`site`, `building`, `administrative_area`, or `generalized_public_site`)
- source type and source identifier
- capture timestamp
- survey identifier or authoritative GIS reference
- operator/reviewer identity as appropriate to the access-controlled evidence system
- canonical payload hash

## Cross-check

Where both survey and authoritative GIS evidence exist, the system calculates spatial difference and records the reconciliation result. A mismatch creates `REVIEW_REQUIRED`; it does not silently select one coordinate.

## Security

The Governor's Residence remains a generalized public-site reference until explicit authorization permits more precise treatment. Sensitive security coordinates must not enter the public evidence view.

## Reporting rule

A geographic node can be visible in the observatory before its coordinate is verified. Visibility means the node exists in the planned reporting grid; it does not mean the site has been surveyed, instrumented, or harvested.
