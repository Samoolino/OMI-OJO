# S6C.8 — Lagos QMS and Laboratory Analysis Readiness Runbook

## Objective
Establish a controlled readiness and evidence pathway for laboratory analysis of samples received through S6C.7. The gate protects sample identity, analytical-method traceability, laboratory competency evidence, quality controls and result provenance.

## Scope
This gate covers analytical readiness and controlled result capture. It does not itself determine potable status, premium status, regulatory compliance or product release.

## Preconditions
1. S6C.7 QMS receipt is accepted for the same event and samples.
2. Sample IDs and condition reconcile with custody records.
3. The analytical scope and analytes are defined.
4. Applicable methods and revisions are identified and approved for the intended use.
5. Laboratory identity and relevant competency/accreditation evidence are recorded where applicable.
6. Instruments and calibration status are acceptable where applicable.
7. Quality-control requirements and acceptance criteria are defined.
8. Result and deviation record structures are available.

## Procedure
1. Create the S6C.8 record and bind it to the S6C.7 QMS case.
2. Reconcile every sample ID before analysis.
3. Record analytical scope, method IDs/revisions and applicable acceptance criteria.
4. Verify laboratory readiness, analyst authorization and instrument/calibration status.
5. Record the QC plan before analysis begins and enter ANALYSIS_READY.
6. Start analysis and record ANALYSIS_IN_PROGRESS with timestamp and analyst identity.
7. Record result references only against the exact sample and method used.
8. Record QC outcomes, deviations and dispositions.
9. Enter RESULTS_RECORDED only when traceability is complete; then move to QMS_REVIEW_PENDING.
10. Preserve raw/result references and integrity digest for S6C.9.

## Evidence package
The package must contain the S6C.7 reference, sample reconciliation, laboratory/method identities and revisions, competency evidence where applicable, instrument/calibration references, QC records, result references, analyst/reviewer identities, deviations/dispositions and an integrity digest.

## Fail-closed controls
Hold or fail the gate for upstream receipt failure, sample identity mismatch, unresolved sample integrity concerns, missing/unapproved methods, missing required laboratory competency evidence, instrument/calibration failure, unresolved QC failure, incomplete result provenance or material deviations.

## Gate interpretation
RESULTS_RECORDED means analytical records exist with traceable provenance. It does **not** mean the sample passed any regulatory or product criterion. QMS review and release decisions remain separate gates.

## Next gate
**S6C.9 — Batch and Seal Release Gate**

Actual laboratory analysis remains NOT_RELEASED until empirical records, result provenance and independent QMS review are captured.
