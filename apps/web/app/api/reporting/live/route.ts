import { NextRequest, NextResponse } from "next/server";\nimport { buildLiveSnapshot } from "../snapshot";

type ProjectContract = {
  project_id: string;
  engagement_id: string;
  site_id: string;
  allowed_sources: string[];
  indicators: string[];
  minimum_evidence: Record<string, "CONTEXTUAL" | "MODELED" | "MEASURED" | "VERIFIED_MEASUREMENT">;
};

const contracts: ProjectContract[] = [
  {
    project_id: "S5-GLOBAL-LAGOS",
    engagement_id: "ENG-S5-LAGOS",
    site_id: "lagos-reference-grid",
    allowed_sources: ["open-meteo-forecast", "open-meteo-archive", "satellite", "authorized-local-gauge"],
    indicators: ["rainfall", "temperature", "relative_humidity", "pressure", "wind_speed"],
    minimum_evidence: {
      rainfall: "CONTEXTUAL",
      temperature: "CONTEXTUAL",
      relative_humidity: "CONTEXTUAL",
      pressure: "CONTEXTUAL",
      wind_speed: "CONTEXTUAL",
    },
  },
  {
    project_id: "S6C",
    engagement_id: "ENG-S6C-LAGOS",
    site_id: "lagos-s6c",
    allowed_sources: ["open-meteo-forecast", "authorized-local-gauge", "field-collector", "water-lab-qms"],
    indicators: ["rainfall"],
    minimum_evidence: { rainfall: "CONTEXTUAL" },
  },
];

const rank: Record<string, number> = {
  CONTEXTUAL: 1,
  MODELED: 2,
  MEASURED: 3,
  VERIFIED_MEASUREMENT: 4,
};

function parseNumber(value: string | null) {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

function distanceKm(aLat: number, aLon: number, bLat: number, bLon: number) {
  const r = 6371;
  const dLat = ((bLat - aLat) * Math.PI) / 180;
  const dLon = ((bLon - aLon) * Math.PI) / 180;
  const x = Math.sin(dLat / 2) ** 2 +
    Math.cos((aLat * Math.PI) / 180) *
    Math.cos((bLat * Math.PI) / 180) *
    Math.sin(dLon / 2) ** 2;
  return 2 * r * Math.asin(Math.sqrt(x));
}

export async function GET(request: NextRequest) {
  const params = request.nextUrl.searchParams;
  const project = params.get("project") || "S5-GLOBAL-LAGOS";
  const site = params.get("site");
  const latitude = parseNumber(params.get("lat"));
  const longitude = parseNumber(params.get("lon"));

  const contract = contracts.find((item) => item.project_id === project);
  if (!contract) {
    return NextResponse.json({ error: "project_reporting_contract_not_found", project }, { status: 404 });
  }

  if (!site || site !== contract.site_id || latitude === null || longitude === null) {
    return NextResponse.json({
      schema_version: "UB-02.LIVE-REPORTING.1",
      state: "LOCATION_INPUT_REQUIRED",
      project,
      required: ["site", "lat", "lon"],
      contract,
      note: "Coordinates must come from an authorized project site/GIS record. The service will not infer a physical site from a city label.",
    }, { status: 422 });
  }

  if (latitude < -90 || latitude > 90 || longitude < -180 || longitude > 180) {
    return NextResponse.json({ error: "invalid_coordinates" }, { status: 422 });
  }

  const url = new URL("https://api.open-meteo.com/v1/forecast");
  url.searchParams.set("latitude", String(latitude));
  url.searchParams.set("longitude", String(longitude));
  url.searchParams.set("hourly", "precipitation,temperature_2m,relative_humidity_2m,pressure_msl,wind_speed_10m");
  url.searchParams.set("forecast_days", "1");
  url.searchParams.set("timezone", "UTC");

  const response = await fetch(url, {
    headers: { Accept: "application/json", "User-Agent": "OMI-OJO/UB-02" },
    cache: "no-store",
  });

  if (!response.ok) {
    return NextResponse.json({ error: "remote_source_error", source: "open-meteo-forecast", status: response.status }, { status: 502 });
  }

  const payload = await response.json();
  const hourly = payload?.hourly;
  if (!hourly?.time) {
    return NextResponse.json({ error: "remote_source_invalid_payload" }, { status: 502 });
  }

  const observations = hourly.time.map((time: string, index: number) => {
    const values = [
      ["rainfall", hourly.precipitation?.[index], "mm"],
      ["temperature", hourly.temperature_2m?.[index], "°C"],
      ["relative_humidity", hourly.relative_humidity_2m?.[index], "%"],
      ["pressure", hourly.pressure_msl?.[index], "hPa"],
      ["wind_speed", hourly.wind_speed_10m?.[index], "km/h"],
    ];

    return values
      .filter(([, value]) => value !== null && value !== undefined)
      .map(([indicator, value, unit]) => {
        const source = "open-meteo-forecast";
        const minimum = contract.minimum_evidence[indicator as string] || "CONTEXTUAL";
        const sourceEvidence = "MODELED";
        const reportable = rank[sourceEvidence] >= rank[minimum as string];

        return {
          observation_id: `om-live-${project}-${site}-${indicator}-${time}`,
          project_id: project,
          site_id: site,
          indicator_id: indicator,
          observed_at: time,
          location: { latitude, longitude },
          location_match: { state: "MATCHED", distance_km: 0 },
          value,
          unit,
          source_id: source,
          provider: "Open-Meteo",
          evidence_class: sourceEvidence,
          reportability: reportable ? "REPORTABLE" : "CONTEXTUAL_ONLY",
          physical_claim_allowed: false,
          methodology_status: "REMOTE_CONTEXT_ONLY",
        };
      });
  }).flat();

  return NextResponse.json({
    schema_version: "UB-02.LIVE-REPORTING.1",
    generated_at: new Date().toISOString(),
    project,
    engagement_id: contract.engagement_id,
    site_id: site,
    source: {
      source_id: "open-meteo-forecast",
      provider: "Open-Meteo",
      endpoint: url.toString(),
      evidence_class: "MODELED",
    },
    location: {
      latitude,
      longitude,
      state: "MATCHED_TO_SUBMITTED_AUTHORIZED_SITE_COORDINATES",
      nearest_source_distance_km: distanceKm(latitude, longitude, latitude, longitude),
    },
    reportability: {
      reportable: observations.filter((o: any) => o.reportability === "REPORTABLE").length,
      contextual_only: observations.filter((o: any) => o.reportability === "CONTEXTUAL_ONLY").length,
      physical_claims_allowed: 0,
    },
    observations,
    release_state: "LIVE_REMOTE_CONTEXT",
    next: [
      "persist canonical observations",
      "run project methodology/reconciliation rules",
      "assemble reporting snapshot",
      "promote only after engagement release gates",
    ],
  });
}
