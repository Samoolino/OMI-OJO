# Blue-Ether Investor Web

Institutional-facing command center for Blue-Ether OS. It is deliberately evidence-first: UI labels distinguish implemented capability, simulation, pending evidence and verified evidence.

## Included

- Interactive WebGL climate/rainfall visualization without a third-party runtime dependency.
- Command Center, Harvest Intelligence, Evidence/DMRV, ESG/GHG and Investor Room surfaces.
- Evidence registry and controlled-scenario interaction.
- Responsive design for desktop and mobile.
- Adapter-ready boundaries for Mapbox/3D geospatial layers and Climatiq carbon calculations.

## Optional production adapters

### Mapbox GL JS
Mapbox GL JS supports interactive 2D/3D maps, custom data, globe projection, rain effects and data-driven layers. It should be added only when the project has an approved Mapbox account/token and licensing configuration.

### Climatiq
Climatiq provides a REST carbon-calculation API with emission factors and audit trails. It should be connected behind a server-side adapter; API keys must never be exposed to browser code. Pin API/data versions and preserve the returned factor/source trail in DMRV evidence.

## Truth boundary

The frontend does not create evidence. Any value marked simulated, modelled, forecast or pending must remain so until backend evidence and review promote its status.

## Local run

```bash
cd apps/web
npm install
npm run dev
```
