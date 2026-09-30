"use client";

import { useEffect, useState } from "react";

type ReadModel = {
  schema_version: string;
  generated_at: string;
  engagement: {
    engagement_id: string;
    project_ids: string[];
    geography: { country: string; region: string; timezone: string };
    sites: string[];
    reporting_frequency: string;
    indicators: string[];
    source_allowlist: string[];
    report_templates: string[];
    blockchain_anchor: boolean;
  };
  release_state: string;
  source_state: string;
  location_state: string;
  reportability: { reportable: number; contextual: number; excluded: number; quarantine: number };
  observations: unknown[];
  snapshots: unknown[];
  next_required_inputs: string[];
};

export default function ReportingPage() {
  const [project, setProject] = useState("S6C");
  const [model, setModel] = useState<ReadModel | null>(null);
  const [loading, setLoading] = useState(false);
  const [liveLoading, setLiveLoading] = useState(false);
  const [site, setSite] = useState(project === "S6C" ? "lagos-s6c" : "lagos-reference-grid");
  const [lat, setLat] = useState("");
  const [lon, setLon] = useState("");
  const [live, setLive] = useState<any | null>(null);

  async function refresh() {
    setLoading(true);
    try {
      const response = await fetch(`/api/reporting?project=${encodeURIComponent(project)}`, { cache: "no-store" });
      setModel(await response.json());
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { setSite(project === "S6C" ? "lagos-s6c" : "lagos-reference-grid"); setLive(null); void refresh(); }, [project]);

  async function refreshLive() {
    setLiveLoading(true);
    try {
      const query = new URLSearchParams({ project, site, lat, lon });
      const response = await fetch(`/api/reporting/live?${query.toString()}`, { cache: "no-store" });
      setLive(await response.json());
    } finally {
      setLiveLoading(false);
    }
  }

  return (
    <main className="shell">
      <div className="main">
        <div className="actions">
          <a className="secondary" href="/">← Control Plane</a>
          <label className="secondary">Project <select value={project} onChange={(event) => setProject(event.target.value)}><option>S6C</option><option>S5-GLOBAL-LAGOS</option></select></label>
          <button className="primary" onClick={() => void refresh()}>{loading ? "Refreshing…" : "Refresh read model"}</button>
          <a className="secondary" href="/api/reporting?project=S5-GLOBAL-LAGOS">Read-model JSON</a>
        </div>

        <section className="hero" style={{ marginTop: 20 }}>
          <div className="panel hero-copy">
            <div className="eyebrow">CANONICAL REPORTING READ MODEL</div>
            <h1>Project data becomes reportable only after it passes the evidence boundary.</h1>
            <p>Provider access, location matching, time matching, quality, reconciliation and evidence class are evaluated before a value enters a report. The frontend reads this governed surface; it does not call environmental providers directly.</p>
          </div>
          <div className="panel section">
            <div className="eyebrow">LIVE STATE</div>
            <h2 style={{ marginTop: 12 }}>{model?.release_state ?? "LOADING"}</h2>
            <p className="muted">{model?.source_state}</p>
            <div className="chain">SOURCE → OBSERVATION → LOCATION/TIME MATCH → QC → REPORTABILITY → SNAPSHOT → REPORT</div>
          </div>
        </section>

        <section className="panel section" style={{ marginTop: 20 }}>
          <div className="eyebrow">REMOTE SOURCE RUNTIME</div>
          <h2>Connect an authorized site coordinate</h2>
          <p className="muted">Open-Meteo is used here only as a governed remote/contextual source. Enter coordinates from the project GIS/site record; the service will not infer a physical site from “Lagos”.</p>
          <div className="actions">
            <label className="secondary">Site <input value={site} onChange={(e) => setSite(e.target.value)} /></label>
            <label className="secondary">Latitude <input inputMode="decimal" value={lat} onChange={(e) => setLat(e.target.value)} placeholder="authorized latitude" /></label>
            <label className="secondary">Longitude <input inputMode="decimal" value={lon} onChange={(e) => setLon(e.target.value)} placeholder="authorized longitude" /></label>
            <button className="primary" onClick={() => void refreshLive()}>{liveLoading ? "Fetching…" : "Fetch governed remote data"}</button>
          </div>
          {live && <div className="scenario" style={{ marginTop: 16 }}>
            <strong>{live.state || live.release_state}</strong> · {live.reportability ? `${live.reportability.reportable} reportable / ${live.reportability.contextual_only} contextual-only` : "location input or source response requires attention"}
            {live.source && <> · {live.source.provider} · {live.source.evidence_class}</>}
          </div>}
          {live?.observations && <div className="table" style={{ marginTop: 16, overflowX: "auto" }}><table><thead><tr><th>Time</th><th>Indicator</th><th>Value</th><th>Source</th><th>Evidence</th><th>State</th></tr></thead><tbody>{live.observations.slice(0, 24).map((o: any) => <tr key={o.observation_id}><td>{o.observed_at}</td><td>{o.indicator_id}</td><td>{o.value} {o.unit}</td><td>{o.provider}</td><td>{o.evidence_class}</td><td>{o.reportability}</td></tr>)}</tbody></table></div>}
        </section>

        {model && (
          <>
            <section className="metric-grid">
              <Metric label="Reportable" value={model.reportability.reportable} />
              <Metric label="Contextual" value={model.reportability.contextual} />
              <Metric label="Excluded" value={model.reportability.excluded} />
              <Metric label="Quarantine" value={model.reportability.quarantine} />
            </section>

            <section className="grid">
              <div className="panel section">
                <div className="eyebrow">{model.engagement.engagement_id}</div>
                <h2>{model.engagement.project_ids.join(" · ")}</h2>
                <p className="muted">{model.engagement.geography.region} · {model.engagement.geography.country} · {model.engagement.geography.timezone}</p>
                <div className="cards">
                  <Info title="Sites" body={model.engagement.sites.join(", ")} />
                  <Info title="Frequency" body={model.engagement.reporting_frequency} />
                  <Info title="Indicators" body={model.engagement.indicators.join(", ")} />
                  <Info title="Sources" body={model.engagement.source_allowlist.join(", ")} />
                  <Info title="Report families" body={model.engagement.report_templates.join(", ")} />
                  <Info title="Anchor" body={model.engagement.blockchain_anchor ? "Enabled after evidence release" : "Not configured"} />
                </div>
              </div>
              <div className="panel section">
                <div className="eyebrow">LOCATION BOUNDARY</div>
                <h2>Match required</h2>
                <p className="muted">{model.location_state}</p>
                <div className="scenario">No coordinates, site measurements, environmental values or evidence claims are inferred when the project boundary is incomplete.</div>
                <div className="chain">{model.next_required_inputs.join(" → ")}</div>
              </div>
            </section>
          </>
        )}

        <footer className="footer">OMI-OJO UB-02 · REPORTABLE ≠ MEASURED ≠ VERIFIED ≠ ANCHORED</footer>
      </div>
    </main>
  );
}

function Metric({ label, value }: { label: string; value: number }) {
  return <div className="panel metric"><div className="label">{label}</div><div className="value">{value}</div><div className="delta">governed read model</div></div>;
}

function Info({ title, body }: { title: string; body: string }) {
  return <div className="mini"><strong>{title}</strong><span>{body}</span></div>;
}
