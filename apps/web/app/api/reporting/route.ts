import { NextRequest, NextResponse } from "next/server";

const engagements = [
  {
    engagement_id: "ENG-S6C-LAGOS",
    project_ids: ["S6C"],
    geography: { country: "NG", region: "Lagos", timezone: "Africa/Lagos" },
    sites: ["lagos-s6c"],
    reporting_frequency: "EVENT_AND_DAILY",
    indicators: ["rainfall", "collection_volume", "water_quality"],
    source_allowlist: ["open-meteo-forecast", "authorized-local-gauge", "field-collector", "water-lab-qms"],
    report_templates: ["PROJECT", "DMRV", "GRANT", "ESG", "VDR", "AUDIT"],
    blockchain_anchor: true,
  },
  {
    engagement_id: "ENG-S5-LAGOS",
    project_ids: ["S5-GLOBAL-LAGOS"],
    geography: { country: "NG", region: "Lagos", timezone: "Africa/Lagos" },
    sites: ["lagos-reference-grid"],
    reporting_frequency: "DAILY",
    indicators: ["rainfall", "temperature", "relative_humidity", "pressure", "wind_speed", "air_quality", "water", "ghg", "esg"],
    source_allowlist: ["open-meteo-forecast", "open-meteo-archive", "satellite", "authorized-local-gauge"],
    report_templates: ["PROJECT", "CLIMATE", "ESG", "GHG", "INSTITUTIONAL"],
    blockchain_anchor: false,
  },
];

export async function GET(request: NextRequest) {
  const project = request.nextUrl.searchParams.get("project");
  const engagement = engagements.find((item) => !project || item.project_ids.includes(project));

  if (!engagement) {
    return NextResponse.json({ error: "reporting_engagement_not_found", project }, { status: 404 });
  }

  // The API intentionally returns an empty live read model until an authorized
  // source adapter supplies canonical observations. It never fabricates values.
  return NextResponse.json({
    schema_version: "UB-02.REPORTING-READ-MODEL.1",
    generated_at: new Date().toISOString(),
    engagement,
    release_state: "NO_LIVE_OBSERVATIONS",
    source_state: "ADAPTERS_CONFIGURED_CREDENTIALS_OR_SITE_ENDPOINTS_REQUIRED",
    location_state: "PROJECT_SITE_COORDINATES_REQUIRED_FOR_MATCHING",
    reportability: {
      reportable: 0,
      contextual: 0,
      excluded: 0,
      quarantine: 0,
    },
    observations: [],
    snapshots: [],\n    refresh: { endpoint: "/api/reporting/refresh", state: "SCHEDULE_BOUNDARY_READY", durable_persistence: "ADAPTER_REQUIRED" },
    next_required_inputs: [
      "authorized_source_endpoint",
      "project_site_coordinates_or_geometry",
      "source_retrieval_credentials_where_required",
      "indicator_methodology_binding",
    ],
  });
}
