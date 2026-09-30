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
  "air-quality-model": {state:"MODELED_CONTEXT", evidenceClass:"MODELED", requiresAuthorizedGis:false, executable:false},
  "satellite-no2": {state:"MODELED_CONTEXT", evidenceClass:"MODELED", requiresAuthorizedGis:false, executable:false},
  "site-rain-gauge": {state:"FIELD_AUTHORIZED_ONLY", evidenceClass:"MEASURED", requiresAuthorizedGis:true, executable:false},
  "site-telemetry": {state:"FIELD_AUTHORIZED_ONLY", evidenceClass:"MEASURED", requiresAuthorizedGis:true, executable:false},
  "water-lab-result": {state:"FIELD_AUTHORIZED_ONLY", evidenceClass:"VERIFIED_MEASUREMENT", requiresAuthorizedGis:true, executable:false},
  "approved-ghg-activity": {state:"AUTHORIZED_SOURCE_REQUIRED", evidenceClass:"MEASURED", requiresAuthorizedGis:true, executable:false},
  "esg-control-register": {state:"AUTHORIZED_SOURCE_REQUIRED", evidenceClass:"MEASURED", requiresAuthorizedGis:true, executable:false}
};
