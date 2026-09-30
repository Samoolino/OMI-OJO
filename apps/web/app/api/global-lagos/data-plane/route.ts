import { NextResponse } from "next/server";
import { lagosNodes } from "../../../global-lagos/nodes";
import { globalLagosIndicators } from "../../../global-lagos/data-plane";
import { nodeReportingProfile } from "../../../global-lagos/reporting";
import { nodeInfrastructure } from "../../../global-lagos/infrastructure";

export const runtime = "nodejs";

export async function GET() {
  const infrastructure = new Map(nodeInfrastructure.map((item) => [item.nodeId, item]));
  return NextResponse.json({
    schema_version: "UB-02.LAGOS.READ-MODEL.1",
    generated_at: new Date().toISOString(),
    authority: "DESCRIPTIVE_READ_MODEL",
    reportability_authority: "CANONICAL_REPORTING_ENGINE",
    nodes: lagosNodes.map((node) => ({
      ...node,
      infrastructure: infrastructure.get(node.id) ?? null,
      reporting: nodeReportingProfile(node.id, node.class),
    })),
    indicators: globalLagosIndicators,
    rules: {
      public_visuals_are_context_only: true,
      candidate_coordinates_are_non_authoritative: true,
      modeled_data_cannot_become_measured_automatically: true,
      frontend_cannot_promote_reportability: true,
    },
  });
}
