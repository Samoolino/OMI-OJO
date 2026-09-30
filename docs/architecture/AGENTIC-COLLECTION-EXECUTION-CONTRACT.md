# Agentic Collection Execution Contract

The orchestration plan is now separated from execution.

## Agent loop

`DISCOVER → PLAN → GATE → EXECUTE → NORMALIZE → QC → CLASSIFY → REPORTABILITY → SNAPSHOT`

### DISCOVER
Read the canonical node, indicator, source and engagement registries.

### PLAN
Generate a deterministic collection action for every applicable node/source/indicator binding.

### GATE
Reject or hold physical/measured/verified collection unless canonical GIS and source authorization requirements are satisfied.

### EXECUTE
Invoke only an explicitly registered executable adapter.

Current executable adapter:
- `open-meteo-forecast`

### NORMALIZE
Adapters return canonical `Observation` objects.

### QC
The observation still passes through the existing reportability/QC path. Adapter execution is not a release decision.

### CLASSIFY
Evidence class remains attached to the observation. Contextual/modelled/satellite/measured/verified classes are not silently promoted.

### REPORTABILITY
The canonical reporting engine determines whether an observation is reportable.

### SNAPSHOT
Only the reporting snapshot layer can establish a durable reporting state.

## Non-negotiable boundaries

1. Candidate public coordinates are not authorization.
2. Missing provider adapters produce HOLD/UNSUPPORTED states, never provider substitution.
3. Remote context data cannot become measured data.
4. Frontend routes remain read-model surfaces.
5. Collection execution does not release reports.
