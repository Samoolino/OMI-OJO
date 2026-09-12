# WAT-002B — Rainfall Validation Model

**State:** S2 — SPECIFIED  
**Purpose:** Empirical validation framework for the 400 L/pod/month financial-model assumption.

## 1. Objective

Quantify whether a 4.0 m² Blue-Ether collection pod can sustainably deliver 400 L/month on an annualized basis in Lagos, while preserving a strict distinction between gross rainfall, harvestable rainfall, quality-approved water and measured delivered water.

## 2. Baseline assumptions

| Variable | Baseline | Status |
|---|---:|---|
| Collection area | 4.0 m² | Engineering assumption |
| Conversion | 1 mm × 1 m² = 1 L | Physical identity |
| First flush | 2.0 mm/event | Engineering assumption; verify in field |
| Example wet month | 300 mm | Illustrative scenario, not a climatological guarantee |
| Example wet events | 15 | Illustrative scenario |
| Example dry month | 40 mm | Illustrative scenario |
| Example dry events | 4 | Illustrative scenario |
| QC rejection | 20% | Financial/model assumption pending telemetry evidence |
| Atmospheric gate | RH >85%, PM2.5 <12 µg/m³ | Operating rule pending field validation |
| Target | 400 L/month | Financial-model assumption to validate |

## 3. Core equations

For each rain event `e`:

`gross_liters_e = rainfall_mm_e × collection_area_m2`

`first_flush_liters_e = min(2.0, rainfall_mm_e) × collection_area_m2`

`post_flush_liters_e = max(0, gross_liters_e - first_flush_liters_e)`

`quality_approved_liters_e = post_flush_liters_e × quality_acceptance_fraction_e`

`delivered_liters_e = min(quality_approved_liters_e, available_storage_capacity_e)`

Monthly yield is the sum of event-level delivered liters. This event-level treatment is mandatory because a 2 mm first-flush penalty is incurred per distinct rain event rather than once per month.

## 4. Illustrative scenarios

### Wet-month example

300 mm × 4 m² = **1,200 L gross**.

15 events × 2 mm × 4 m² = **120 L first-flush diversion** (not 114 L; the corrected value is used here).

If 20% of post-flush water fails the assumed QC gate:

`(1,200 − 120) × 0.80 = 864 L`

This is an illustrative model output, not measured production.

### Dry-month example

40 mm × 4 m² = **160 L gross**.

4 events × 2 mm × 4 m² = **32 L first-flush diversion**.

At 80% quality acceptance:

`(160 − 32) × 0.80 = 102.4 L`

## 5. Annualized validation method

The financial model must not average only one wet-month and one dry-month example. Validation shall use a complete 12-month rainfall series for the selected Lagos reference location, event separation rules, observed/estimated environmental gates, pod storage constraints and telemetry.

Required outputs:

- monthly rainfall mm;
- number of distinct rain events;
- first-flush loss;
- gross theoretical liters;
- atmospheric/QC rejected liters;
- storage-limited liters;
- measured collected liters;
- measured released/usable liters;
- annual total and monthly P10/P50/P90 yield;
- fraction of months ≥400 L;
- annualized average liters/pod/month;
- confidence interval and data-quality score.

## 6. Validation verdict logic

The 400 L assumption is **VALIDATED** only when the approved historical/modelled dataset plus field telemetry demonstrates the agreed acceptance criterion. Until then the status is **ASSUMPTION — NOT BANKABLE**.

Recommended acceptance criterion:

1. ≥12 months of location-matched rainfall observations or a documented climatological dataset;
2. ≥3 months of pilot pod telemetry for calibration, with ≥6 months preferred;
3. event-level first-flush accounting;
4. independent water-quality/QC evidence;
5. reproducible calculation notebook or test suite;
6. signed technical review before the financial model upgrades the assumption from S2 to S4.

## 7. Data lineage

Every validation run must store dataset source, observation period, geographic reference, units, preprocessing version, model version, execution timestamp and reviewer.

**Claim boundary:** forecast rainfall is never substituted for measured rainfall in DMRV or audited production records.
