import { lagosNodes } from "./nodes";
import { globalLagosIndicators } from "./data-plane";
import { nodeReportingProfile } from "./reporting";

export type SourceCapabilityState =
  | "CONTEXT_CAPABLE"
  | "MODELED_CONTEXT"
  | "FIELD_AUTHORIZED_ONLY"
  | "AUTHORIZED_SOURCE_REQUIRED";

export type CollectionPlanState =
  | "CONTEXT_PLAN"
  | "READY_FOR_AUTHORIZED_COLLECTION"
  | "BLOCKED_PENDING_GIS"
  | "UNSUPPORTED_ADAPTER";

export type NodeSourceBinding = {
  nodeId: string;
  nodeClass: (typeof lagosNodes)[number]["class"];
  indicatorId: string;
  sourceId: string;
  evidenceClass: string;
  sourceCapability: SourceCapabilityState;
  refresh: (typeof globalLagosIndicators)[number]["refresh"];
  requiresAuthorizedGis: boolean;
  authorizationRequired: boolean;
  qcRule: string;
  reportFamilies: string[];
  state: CollectionPlanState;
};

const sourceCapabilities: Record<string, {state: SourceCapabilityState; evidenceClass: string; requiresAuthorizedGis: boolean; executable: boolean}> = {
  "open-meteo-forecast": {state:"CONTEXT_CAPABLE", evidenceClass:"MODELED", requiresAuthorizedGis:false, executable:true},
  "satellite-derived-context": {state:"CONTEXT_CAPABLE", evidenceClass:"SATELLITE", requiresAuthorizedGis:false, executable:false},
  "air-quality-model": {state:"MODELED_CONTEXT", evidenceClass:"MODELED", requiresAuthorizedGis:false},
  "satellite-no2": {state:"MODELED_CONTEXT", evidenceClass:"MODELED", requiresAuthorizedGis:false},
  "site-rain-gauge": {state:"FIELD_AUTHORIZED_ONLY", evidenceClass:"MEASURED", requiresAuthorizedGis:true, executable:false},
  "site-telemetry": {state:"FIELD_AUTHORIZED_ONLY", evidenceClass:"MEASURED", requiresAuthorizedGis:true},
  "water-lab-result": {state:"FIELD_AUTHORIZED_ONLY", evidenceClass:"VERIFIED_MEASUREMENT", requiresAuthorizedGis:true},
  "approved-ghg-activity": {state:"AUTHORIZED_SOURCE_REQUIRED", evidenceClass:"MEASURED", requiresAuthorizedGis:true},
  "esg-control-register": {state:"AUTHORIZED_SOURCE_REQUIRED", evidenceClass:"MEASURED", requiresAuthorizedGis:true}
};

const bindingsByClass: Record<string, Record<string,string[]>> = {
  LCDA_REFERENCE: {
    rainfall:["open-meteo-forecast","site-rain-gauge"], temperature:["open-meteo-forecast"],
    relative_humidity:["open-meteo-forecast"], wind_speed:["open-meteo-forecast"],
    solar_radiation:["open-meteo-forecast","satellite-derived-context"], air_quality:["air-quality-model"],
    no2:["satellite-no2"], pm25:["air-quality-model"], water_quality:["water-lab-result"],
    collection_volume:["site-telemetry"], ghg_activity_data:["approved-ghg-activity"], esg_controls:["esg-control-register"]
  },
  STATE_INSTITUTION: {
    rainfall:["open-meteo-forecast","site-rain-gauge"], temperature:["open-meteo-forecast"],
    relative_humidity:["open-meteo-forecast"], wind_speed:["open-meteo-forecast"],
    solar_radiation:["open-meteo-forecast","satellite-derived-context"], air_quality:["air-quality-model"],
    no2:["satellite-no2"], pm25:["air-quality-model"], water_quality:[],
    collection_volume:["site-telemetry"], ghg_activity_data:["approved-ghg-activity"], esg_controls:["esg-control-register"]
  },
  ENVIRONMENTAL_REFERENCE: {
    rainfall:["open-meteo-forecast"], temperature:["open-meteo-forecast"],
    relative_humidity:["open-meteo-forecast"], wind_speed:["open-meteo-forecast"],
    solar_radiation:["open-meteo-forecast","satellite-derived-context"], air_quality:["air-quality-model"],
    no2:["satellite-no2"], pm25:["air-quality-model"], water_quality:["water-lab-result"],
    collection_volume:[], ghg_activity_data:[], esg_controls:["esg-control-register"]
  }
};

export const buildGlobalLagosCollectionPlan = (): NodeSourceBinding[] =>
  lagosNodes.flatMap((node) =>
    globalLagosIndicators.flatMap((indicator) =>
      (bindingsByClass[node.class][indicator.id] ?? []).map((sourceId): NodeSourceBinding => {
        const capability = sourceCapabilities[sourceId];
        const requiresAuthorizedGis = capability.requiresAuthorizedGis;
        const state: CollectionPlanState =
          !capability ? "UNSUPPORTED_ADAPTER" :
          requiresAuthorizedGis
            ? "BLOCKED_PENDING_GIS"
            : "CONTEXT_PLAN";
        return {
          nodeId: node.id,
          nodeClass: node.class,
          indicatorId: indicator.id,
          sourceId,
          evidenceClass: capability.evidenceClass,
          sourceCapability: capability.state,
          refresh: indicator.refresh,
          requiresAuthorizedGis,
          authorizationRequired: requiresAuthorizedGis || sourceId === "esg-control-register",
          qcRule: requiresAuthorizedGis ? "location_match + time_match + qc + custody/authorization" : "provider provenance + timestamp + schema/QC",
          reportFamilies: nodeReportingProfile(node.id, node.class).reportFamilies,
          state
        };
      })
    )
  );

export const globalLagosOrchestrationSummary = () => {
  const plan = buildGlobalLagosCollectionPlan();
  return {
    schema_version: "UB-02.LAGOS.ORCHESTRATION.1",
    node_count: lagosNodes.length,
    indicator_count: globalLagosIndicators.length,
    binding_count: plan.length,
    nodes_with_bindings: new Set(plan.map((x) => x.nodeId)).size,
    states: {
      context: plan.filter((x) => x.state === "CONTEXT_PLAN").length,
      ready_for_authorized_collection: plan.filter((x) => x.state === "READY_FOR_AUTHORIZED_COLLECTION").length,
      blocked_pending_gis: plan.filter((x) => x.state === "BLOCKED_PENDING_GIS").length,
      unsupported_adapter: plan.filter((x) => x.state === "UNSUPPORTED_ADAPTER").length
    },
    rules: [
      "Pending GIS blocks physical/field collection.",
      "Candidate public coordinates never authorize field collection.",
      "Modeled, satellite, measured and verified evidence classes remain distinct.",
      "Frontend consumes this plan as a read model; it cannot promote reportability."
    ],
    plan
  };
};
