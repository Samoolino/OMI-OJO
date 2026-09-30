import { createHash } from "crypto";

export type CanonicalLiveObservation = {
  observation_id: string;
  project_id: string;
  site_id: string;
  indicator_id: string;
  observed_at: string;
  location: { latitude: number; longitude: number };
  value: number;
  unit: string;
  source_id: string;
  evidence_class: string;
  reportability: "REPORTABLE" | "CONTEXTUAL_ONLY";
};

export function buildLiveSnapshot(input: {
  projectId: string;
  siteId: string;
  reportFamily: string;
  periodStart: string;
  periodEnd: string;
  observations: CanonicalLiveObservation[];
}) {
  const reportable = input.observations.filter((o) => o.reportability === "REPORTABLE").map((o) => o.observation_id).sort();
  const contextual = input.observations.filter((o) => o.reportability === "CONTEXTUAL_ONLY").map((o) => o.observation_id).sort();
  const indicators = [...new Set(input.observations.map((o) => o.indicator_id))].sort();
  const sources = [...new Set(input.observations.map((o) => o.source_id))].sort();

  const canonical = {
    schema_version: "UB-02.REPORTING-SNAPSHOT.1",
    project_id: input.projectId,
    site_ids: [input.siteId],
    report_family: input.reportFamily,
    reporting_period_start: input.periodStart,
    reporting_period_end: input.periodEnd,
    reportable_observation_ids: reportable,
    contextual_observation_ids: contextual,
    excluded_observation_ids: [],
    indicator_ids: indicators,
    source_ids: sources,
    release_state: "DRAFT",
  };

  const deterministicHash = createHash("sha256")
    .update(JSON.stringify(canonical))
    .digest("hex");

  return {
    ...canonical,
    snapshot_id: `RS-${deterministicHash.slice(0, 16)}`,
    created_at: new Date().toISOString(),
    deterministic_hash: deterministicHash,
    persistence_state: "RUNTIME_ONLY",
  };
}
