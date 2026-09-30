export type NodeReportingProfile = {
  nodeId: string;
  reportFamilies: string[];
  primaryIndicators: string[];
  minimumEvidence: string[];
  releaseRule: string;
};

export const nodeReportingProfile = (nodeId: string, stateClass: string): NodeReportingProfile => {
  const environmental = stateClass === "ENVIRONMENTAL_REFERENCE";
  const institutional = stateClass === "STATE_INSTITUTION";
  return {
    nodeId,
    reportFamilies: environmental
      ? ["project_status","climate","esg","dmrv_evidence","regulatory_audit"]
      : institutional
        ? ["project_status","climate","esg","dmrv_evidence","regulatory_audit"]
        : ["project_status","environmental_data","climate","water","esg","ghg","dmrv_evidence"],
    primaryIndicators: environmental
      ? ["rainfall","temperature","humidity","wind","vegetation_context"]
      : ["rainfall","temperature","relative_humidity","pressure","wind_speed","air_quality"],
    minimumEvidence: environmental
      ? ["authorized_gis","approved_visual_reference","field_evidence_when_claimed"]
      : ["authorized_gis","source_provenance","location_match","time_match","qc"],
    releaseRule: "Reference and modelled data may inform context; measured or verified claims require their corresponding authorized evidence class and QC gate."
  };
};
