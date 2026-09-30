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

  async function refresh() {
    setLoading(true);
    try {
      const response = await fetch(`/api/reporting?project=${encodeURIComponent(project)}`, { cache: "no-store" });
      setModel(await response.json());
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { void refresh(); }, [project]);

  return (
    <main className="shell">
      <div className="main">
        <div className="actions">
          <a className="secondary" href="/">← Control Plane</a>
          <label className="secondary">Project <select value={project} onChange={(event) => setProject(event.target.value)}><option>S6C</option><option>S5-GLOBAL-LAGOS</option></select></label>
          <button className="primary" onClick={() => void refresh()}>{loading ? "Refreshing…" : "Refresh read model"}</button>
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
