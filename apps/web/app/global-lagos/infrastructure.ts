export type NodeInfrastructure = {
  nodeId: string;
  venueType: "LCDA_CIVIC" | "STATE_INSTITUTION" | "ENVIRONMENTAL_REFERENCE";
  infrastructure: string[];
  climateSignals: string[];
  esgControls: string[];
  evidencePath: string[];
  dataMode: "REFERENCE_ONLY" | "READY_FOR_AUTHORIZED_DEPLOYMENT";
};

export const nodeInfrastructure: NodeInfrastructure[] = [
  ...Array.from({length:37},(_,i)=>({
    nodeId: `LGA${String([1,2,3,3,3,3,4,5,6,6,7,7,8,8,8,9,10,10,11,11,12,12,12,12,12,13,13,14,15,16,17,17,18,19,19,20,20][i]).padStart(2,"0")}-LCDA${String([1,1,1,2,3,4,1,1,1,2,1,2,1,2,3,1,1,2,1,2,1,2,3,4,5,1,2,1,1,1,1,2,1,1,2,1,2][i]).padStart(2,"0")}`,
    venueType:"LCDA_CIVIC" as const,
    infrastructure:["site authorization","rain gauge / telemetry mount","secure evidence capture point","power + communications assessment"],
    climateSignals:["rainfall","temperature","humidity","wind","solar context"],
    esgControls:["site-owner authorization","operator custody","maintenance log","incident / exception register"],
    evidencePath:["source snapshot","location/time match","QC result","evidence package","DMRV review"],
    dataMode:"REFERENCE_ONLY" as const
  })),
  {nodeId:"STATE-VENUE-01",venueType:"STATE_INSTITUTION",infrastructure:["generalized public-site reference","authorization boundary","security review","no public precision coordinate"],climateSignals:["rainfall context","heat context","air-quality context"],esgControls:["security authorization","privacy / safety review","access control","audit trail"],evidencePath:["public reference","authorization record","approved site evidence"],dataMode:"REFERENCE_ONLY"},
  {nodeId:"STATE-VENUE-02",venueType:"STATE_INSTITUTION",infrastructure:["institutional monitoring point","communications/power assessment","secure evidence capture"],climateSignals:["rainfall","temperature","humidity","air quality"],esgControls:["institutional authorization","custody","maintenance","audit trail"],evidencePath:["source snapshot","location/time match","QC","DMRV review"],dataMode:"REFERENCE_ONLY"},
  {nodeId:"STATE-VENUE-03",venueType:"ENVIRONMENTAL_REFERENCE",infrastructure:["environmental reference site","public visual reference","future biodiversity/ecosystem evidence boundary"],climateSignals:["rainfall","heat","humidity","wind","vegetation context"],esgControls:["site stewardship","access controls","environmental safeguards","evidence custody"],evidencePath:["public visual reference","authorized GIS","field evidence","DMRV review"],dataMode:"REFERENCE_ONLY"}
];
