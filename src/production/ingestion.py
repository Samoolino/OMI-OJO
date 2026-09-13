"""Deterministic, provenance-preserving HTTP ingestion primitives.

This module deliberately does not promote external data to VERIFIED. It only
creates immutable source observations/snapshots that downstream DMRV gates can
review and reconcile.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class Observation:
    observation_id: str
    source_id: str
    provider: str
    kind: str
    variable: str
    value: float
    unit: str
    observed_at: str
    retrieved_at: str
    latitude: float | None
    longitude: float | None
    quality: str
    status: str = "INGESTED"

    def canonical(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))

    @property
    def evidence_hash(self) -> str:
        return hashlib.sha256(self.canonical().encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class ForecastSnapshot:
    snapshot_id: str
    source_id: str
    provider: str
    retrieved_at: str
    latitude: float
    longitude: float
    payload: dict[str, Any]

    def canonical(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))

    @property
    def evidence_hash(self) -> str:
        return hashlib.sha256(self.canonical().encode("utf-8")).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def deterministic_id(prefix: str, canonical: str) -> str:
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:24]
    return f"{prefix}_{digest}"


def fetch_json(url: str, timeout_seconds: int = 20) -> dict[str, Any]:
    """Fetch JSON without silently retrying or mutating the request."""
    request = Request(url, headers={"Accept": "application/json", "User-Agent": "Blue-Ether-OS/1.0"})
    with urlopen(request, timeout=timeout_seconds) as response:  # noqa: S310 - URL is configured by operator
        if response.status != 200:
            raise RuntimeError(f"source returned HTTP {response.status}")
        payload = json.loads(response.read().decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("source response must be a JSON object")
    return payload


def open_meteo_forecast_snapshot(
    latitude: float,
    longitude: float,
    *,
    source_id: str = "open-meteo-forecast",
    base_url: str = "https://api.open-meteo.com/v1/forecast",
    extra_params: dict[str, str] | None = None,
) -> ForecastSnapshot:
    """Create an immutable forecast snapshot for a site.

    The payload is retained exactly as returned. A new retrieval always creates
    a new snapshot; historical snapshots must never be overwritten.
    """
    from urllib.parse import urlencode

    params = {
        "latitude": str(latitude),
        "longitude": str(longitude),
        "hourly": "precipitation,temperature_2m,relative_humidity_2m,pressure_msl,wind_speed_10m",
        "daily": "precipitation_sum",
        "timezone": "UTC",
    }
    if extra_params:
        params.update(extra_params)
    url = f"{base_url}?{urlencode(params)}"
    payload = fetch_json(url)
    retrieved_at = utc_now()
    canonical_input = json.dumps(
        {"source_id": source_id, "retrieved_at": retrieved_at, "latitude": latitude, "longitude": longitude, "payload": payload},
        sort_keys=True,
        separators=(",", ":"),
    )
    return ForecastSnapshot(
        snapshot_id=deterministic_id("fcst", canonical_input),
        source_id=source_id,
        provider="Open-Meteo",
        retrieved_at=retrieved_at,
        latitude=latitude,
        longitude=longitude,
        payload=payload,
    )


def rainfall_observation(
    *,
    source_id: str,
    provider: str,
    observed_at: str,
    rainfall_mm: float,
    latitude: float | None = None,
    longitude: float | None = None,
    quality: str = "UNASSESSED",
) -> Observation:
    if rainfall_mm < 0:
        raise ValueError("rainfall cannot be negative")
    retrieved_at = utc_now()
    seed = json.dumps(
        {"source_id": source_id, "observed_at": observed_at, "rainfall_mm": rainfall_mm, "latitude": latitude, "longitude": longitude},
        sort_keys=True,
        separators=(",", ":"),
    )
    return Observation(
        observation_id=deterministic_id("obs", seed),
        source_id=source_id,
        provider=provider,
        kind="STATION",
        variable="precipitation",
        value=rainfall_mm,
        unit="mm",
        observed_at=observed_at,
        retrieved_at=retrieved_at,
        latitude=latitude,
        longitude=longitude,
        quality=quality,
    )
