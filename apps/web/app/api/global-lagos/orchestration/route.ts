import { NextResponse } from "next/server";
import { globalLagosOrchestrationSummary } from "../../../global-lagos/orchestration";

export const runtime = "nodejs";

export async function GET() {
  return NextResponse.json(globalLagosOrchestrationSummary(), {
    headers: { "Cache-Control": "no-store" }
  });
}
