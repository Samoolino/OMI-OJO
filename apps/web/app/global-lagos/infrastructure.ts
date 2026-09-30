export type NodeInfrastructure = {
  nodeId: string;
  venueType: "LCDA_CIVIC" | "STATE_INSTITUTION" | "ENVIRONMENTAL_REFERENCE";
  infrastructure: string[];
  climateSignals: string[];
  esgControls: string[];
  evidencePath: string[];
  dataMode: "REFERENCE_ONLY" | "READY_FOR_AUTHORIZED_DEPLOYMENT";
};

const lcdaIds = ["LGA01-LCDA01","LGA02-LCDA01","LGA03-LCDA01","LGA03-LCDA02","LGA03-LCDA03","LGA03-LCDA04","LGA04-LCDA01","LGA05-LCDA01","LGA06-LCDA01","LGA06-LCDA02","LGA07-LCDA01","LGA07-LCDA02","LGA08-LCDA01","LGA08-LCDA02","LGA08-LCDA03","LGA09-LCDA01","LGA10-LCDA01","LGA10-LCDA02","LGA11-LCDA01","LGA11-LCDA02","LGA12-LCDA01","LGA12-LCDA02","LGA12-LCDA03","LGA12-LCDA04","LGA12-LCDA05","LGA13-LCDA01","LGA13-LCDA02","LGA14-LCDA01","LGA15-LCDA01","LGA16-LCDA01","LGA17-LCDA01","LGA17-LCDA02","LGA18-LCDA01","LGA19-LCDA01","LGA19-LCDA02","LGA20-LCDA01","LGA20-LCDA02"];
const lcdaInfrastructure = lcdaIds.map((nodeId) => ({
  nodeId,
  venueType: "LCDA_CIVIC" as const,
  infrastructure: ["site authorization","rain gauge / telemetry mount","secure evidence capture point","power + communications assessment"],
  climateSignals: ["rainfall","temperature","humidity","wind","solar context"],
  esgControls: ["site-owner authorization","operator custody","maintenance log","incident / exception register"],
  evidencePath: ["source snapshot","location/time match","QC result","evidence package","DMRV review"],
  dataMode: "REFERENCE_ONLY" as const
}));

export const nodeInfrastructure: NodeInfrastructure[] = [...lcdaInfrastructure, {nodeId:"STATE-VENUE-01",venueType:"STATE_INSTITUTION",infrastructure:["generalized public-site reference","authorization boundary","security review","no public precision coordinate"],climateSignals:["rainfall context","heat context","air-quality context"],esgControls:["security authorization","privacy / safety review","access control","audit trail"],evidencePath:["public reference","authorization record","approved site evidence"],dataMode:"REFERENCE_ONLY"},
  {nodeId:"STATE-VENUE-02",venueType:"STATE_INSTITUTION",infrastructure:["institutional monitoring point","communications/power assessment","secure evidence capture"],climateSignals:["rainfall","temperature","humidity","air quality"],esgControls:["institutional authorization","custody","maintenance","audit trail"],evidencePath:["source snapshot","location/time match","QC","DMRV review"],dataMode:"REFERENCE_ONLY"},
  {nodeId:"STATE-VENUE-03",venueType:"ENVIRONMENTAL_REFERENCE",infrastructure:["environmental reference site","public visual reference","future biodiversity/ecosystem evidence boundary"],climateSignals:["rainfall","heat","humidity","wind","vegetation context"],esgControls:["site stewardship","access controls","environmental safeguards","evidence custody"],evidencePath:["public visual reference","authorized GIS","field evidence","DMRV review"],dataMode:"REFERENCE_ONLY"}
];
