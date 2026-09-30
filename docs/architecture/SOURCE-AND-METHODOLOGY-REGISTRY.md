# OMI-OJO Source & Methodology Registry

## Source Registry

Every source is registered before it is used in a reportable pipeline.

Required fields:

- `source_id`
- provider/owner
- source type
- geography
- data domain
- temporal/spatial resolution
- transport/API
- license/terms
- retrieval timestamp
- source version
- validation state
- evidence class
- quality rules
- responsible owner

### Source classes

- **PRIMARY_OBSERVED** — controlled sensor/field/lab evidence.
- **AUTHORITATIVE_EXTERNAL** — official/public institutional datasets.
- **SATELLITE** — remote sensing products.
- **COMMERCIAL_API** — licensed provider/API data.
- **MODELLED** — numerical/model output.
- **PROXY** — indirect evidence, explicitly labelled.

No source class is silently upgraded by aggregation or UI presentation.

## Methodology Registry

Required fields:

- `methodology_id`
- name/version
- purpose
- applicable geography
- applicable indicators
- inputs
- formula/procedure
- assumptions
- uncertainty
- QC rules
- reconciliation rules
- evidence requirements
- reviewer requirements
- permitted claims
- prohibited claims
- supersession/effective dates

## Indicator contract

Every indicator references:

`indicator_id -> source(s) -> methodology -> calculation -> evidence -> claim -> report`

## Verified-data policy

"Verified" is a controlled state, not a source category. A source may be authoritative without being verified for a particular project; a project observation may be verified only after the applicable QC/reconciliation/review gate passes.

## Climate & ESG mapping

Source and methodology records must support mapping into:

- climate
- water
- air
- energy
- land/agriculture
- biodiversity
- built environment
- GHG
- ESG E/S/G
- climate risk
- institutional reporting
