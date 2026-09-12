# WAT-003 — First-Flush Protocol

**State:** S2 — SPECIFIED

## Rule

The first **2.0 mm of each distinct rain event** is diverted before collection proceeds, subject to engineering verification and calibration.

## Event definition

A new event begins after the configured dry-gap threshold has elapsed. The threshold must be defined and versioned in the pod firmware/configuration; it must not be inferred retrospectively.

## Accounting

For a 4.0 m² collection area, 2.0 mm corresponds to **8.0 L** of theoretical first-flush diversion per event.

## Controls

- record event start/end;
- record rainfall depth;
- record diverted volume;
- record bypass status;
- record valve/sensor faults;
- reconcile physical diversion against calculated diversion;
- route rejected water according to the approved environmental/QMS procedure.

## Verification

Field calibration must demonstrate actual diversion volume and valve timing under representative rainfall conditions before the protocol is treated as S4 verified.
