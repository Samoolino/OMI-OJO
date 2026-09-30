export type SourceState = "AVAILABLE_FOR_CONTEXT" | "PLANNED_AUTHORIZED_SOURCE" | "FIELD_VALIDATION_REQUIRED";
export type EvidenceClass = "CONTEXTUAL" | "MODELED" | "SATELLITE" | "MEASURED" | "VERIFIED_MEASUREMENT";

export type IndicatorSpec = {
  id: string;
  label: string;
  unit: string;
  domain: "CLIMATE" | "AIR_QUALITY" | "WATER" | "ESG" | "GHG";
  preferredSources: string[];
  evidenceClass: EvidenceClass;
  sourceState: SourceState;
  refresh: "HOURLY" | "DAILY" | "EVENT" | "PERIODIC";
};

export const globalLagosIndicators: IndicatorSpec[] = [
  {id:"rainfall",label:"Rainfall",unit:"mm",domain:"CLIMATE",preferredSources:["Open-Meteo forecast/archive","authorized local gauge"],evidenceClass:"CONTEXTUAL",sourceState:"AVAILABLE_FOR_CONTEXT",refresh:"DAILY"},
  {id:"temperature",label:"Air temperature",unit:"°C",domain:"CLIMATE",preferredSources:["Open-Meteo forecast/archive","authorized local station"],evidenceClass:"CONTEXTUAL",sourceState:"AVAILABLE_FOR_CONTEXT",refresh:"DAILY"},
  {id:"relative_humidity",label:"Relative humidity",unit:"%",domain:"CLIMATE",preferredSources:["Open-Meteo forecast/archive","authorized local station"],evidenceClass:"CONTEXTUAL",sourceState:"AVAILABLE_FOR_CONTEXT",refresh:"DAILY"},
  {id:"wind_speed",label:"Wind speed",unit:"m/s",domain:"CLIMATE",preferredSources:["Open-Meteo forecast/archive","authorized local station"],evidenceClass:"CONTEXTUAL",sourceState:"AVAILABLE_FOR_CONTEXT",refresh:"DAILY"},
  {id:"solar_radiation",label:"Solar radiation",unit:"W/m²",domain:"CLIMATE",preferredSources:["Open-Meteo","satellite-derived dataset"],evidenceClass:"CONTEXTUAL",sourceState:"AVAILABLE_FOR_CONTEXT",refresh:"DAILY"},
  {id:"air_quality",label:"Air quality index / particulate context",unit:"provider-defined",domain:"AIR_QUALITY",preferredSources:["Open-Meteo air quality","authorized local sensor"],evidenceClass:"MODELED",sourceState:"AVAILABLE_FOR_CONTEXT",refresh:"HOURLY"},
  {id:"no2",label:"Atmospheric NO₂",unit:"µg/m³",domain:"AIR_QUALITY",preferredSources:["CAMS/model","Sentinel-5P/TROPOMI"],evidenceClass:"MODELED",sourceState:"AVAILABLE_FOR_CONTEXT",refresh:"DAILY"},
  {id:"pm25",label:"PM2.5",unit:"µg/m³",domain:"AIR_QUALITY",preferredSources:["air-quality model","authorized local sensor"],evidenceClass:"MODELED",sourceState:"AVAILABLE_FOR_CONTEXT",refresh:"HOURLY"},
  {id:"water_quality",label:"Water quality",unit:"lab-specific",domain:"WATER",preferredSources:["authorized field sampler","water laboratory QMS"],evidenceClass:"VERIFIED_MEASUREMENT",sourceState:"FIELD_VALIDATION_REQUIRED",refresh:"EVENT"},
  {id:"collection_volume",label:"Collection volume",unit:"site-specific",domain:"ESG",preferredSources:["authorized field telemetry","custody record"],evidenceClass:"MEASURED",sourceState:"FIELD_VALIDATION_REQUIRED",refresh:"EVENT"},
  {id:"ghg_activity_data",label:"GHG activity data",unit:"method-specific",domain:"GHG",preferredSources:["approved activity-data source"],evidenceClass:"MEASURED",sourceState:"FIELD_VALIDATION_REQUIRED",refresh:"PERIODIC"},
  {id:"esg_controls",label:"ESG control status",unit:"status",domain:"ESG",preferredSources:["authorization register","maintenance log","incident register"],evidenceClass:"MEASURED",sourceState:"PLANNED_AUTHORIZED_SOURCE",refresh:"PERIODIC"}
];

export const nodeDataPlane = {
  version: "UB-02.LAGOS.DATA-PLANE.1",
  defaultRefresh: "DAILY",
  coordinateRule: "AUTHORIZED_GIS_REQUIRED",
  frontendRule: "READ_MODEL_ONLY",
  sourceRule: "PROVIDER_OUTPUT_REMAINS_IN_ITS_EVIDENCE_CLASS",
  promotionRule: "NO_AUTOMATIC_PROMOTION",
  indicators: globalLagosIndicators
} as const;
