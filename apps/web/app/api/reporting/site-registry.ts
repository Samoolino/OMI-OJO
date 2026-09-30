export type SiteAuthorization = {
  site_id: string;
  project_ids: string[];
  status: "AUTHORIZED" | "PENDING_AUTHORIZED_GIS";
  latitude: number | null;
  longitude: number | null;
  coordinate_source: string | null;
  coordinate_version: string | null;
};

export const siteRegistry: SiteAuthorization[] = [
  {
    site_id: "lagos-reference-grid",
    project_ids: ["S5-GLOBAL-LAGOS"],
    status: "PENDING_AUTHORIZED_GIS",
    latitude: null,
    longitude: null,
    coordinate_source: null,
    coordinate_version: null,
  },
  {
    site_id: "lagos-s6c",
    project_ids: ["S6C"],
    status: "PENDING_AUTHORIZED_GIS",
    latitude: null,
    longitude: null,
    coordinate_source: null,
    coordinate_version: null,
  },
];

export function resolveAuthorizedSite(projectId: string, siteId: string) {
  const site = siteRegistry.find((item) => item.site_id === siteId);
  if (!site) return { state: "SITE_NOT_REGISTERED" as const, site: null };
  if (!site.project_ids.includes(projectId)) {
    return { state: "SITE_PROJECT_MISMATCH" as const, site };
  }
  if (site.status !== "AUTHORIZED") {
    return { state: "SITE_LOCATION_NOT_AUTHORIZED" as const, site };
  }
  if (site.latitude === null || site.longitude === null) {
    return { state: "SITE_COORDINATES_MISSING" as const, site };
  }
  if (!site.coordinate_source || !site.coordinate_version) {
    return { state: "SITE_COORDINATE_PROVENANCE_MISSING" as const, site };
  }
  return { state: "AUTHORIZED" as const, site };
}
