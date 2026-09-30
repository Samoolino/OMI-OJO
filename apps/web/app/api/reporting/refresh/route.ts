import { NextRequest, NextResponse } from "next/server";

const engagements = [
  { engagement_id: "ENG-S5-LAGOS", project: "S5-GLOBAL-LAGOS", site: "lagos-reference-grid", cadence: "DAILY" },
  { engagement_id: "ENG-S6C-LAGOS", project: "S6C", site: "lagos-s6c", cadence: "EVENT_AND_DAILY" },
];

function authorized(request: NextRequest) {
  const configured = process.env.REPORTING_REFRESH_SECRET;
  if (!configured) return process.env.NODE_ENV !== "production";
  return request.headers.get("authorization") === `Bearer ${configured}`;
}

export async function POST(request: NextRequest) {
  if (!authorized(request)) {
    return NextResponse.json({ error: "refresh_authorization_required" }, { status: 401 });
  }

  const body = await request.json().catch(() => ({}));
  const project = typeof body?.project === "string" ? body.project : null;
  const selected = engagements.filter((e) => !project || e.project === project);

  if (!selected.length) {
    return NextResponse.json({ error: "reporting_engagement_not_found", project }, { status: 404 });
  }

  return NextResponse.json({
    schema_version: "UB-02.REPORTING-REFRESH.1",
    state: "SCHEDULE_ACCEPTED",
    accepted_at: new Date().toISOString(),
    engagements: selected.map((e) => ({
      ...e,
      source_runtime: `/api/reporting/live?project=${encodeURIComponent(e.project)}&site=${encodeURIComponent(e.site)}`,
      persistence: "DURABLE_STORE_ADAPTER_REQUIRED",
      release_gate: "NOT_RELEASED",
    })),
    note: "This endpoint is a scheduler boundary. Production deployment must provide REPORTING_REFRESH_SECRET and a durable persistence adapter before automatic publication.",
  });
}
