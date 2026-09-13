"""Deterministic, provenance-preserving HTTP ingestion primitives.

External data is immutable evidence input. Ingestion state and data status are
kept distinct so downstream DMRV can require measured telemetry explicitly.
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
    data_status: str = "MEASURED"
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
    """Create an immutable forecast snapshot; never overwrite prior snapshots."""
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
    payload = fetch_json(f"{base_url}?{urlencode(params)}")
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
    kind: str = "STATION",
    data_status: str = "MEASURED",
) -> Observation:
    """Normalize one rainfall value while preserving its evidence classification."""
    if rainfall_mm < 0:
        raise ValueError("rainfall cannot be negative")
    retrieved_at = utc_now()
    seed = json.dumps(
        {
            "source_id": source_id,
            "observed_at": observed_at,
            "rainfall_mm": rainfall_mm,
            "latitude": latitude,
            "longitude": longitude,
            "kind": kind,
            "data_status": data_status,
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return Observation(
        observation_id=deterministic_id("obs", seed),
        source_id=source_id,
        provider=provider,
        kind=kind,
        variable="precipitation",
        value=rainfall_mm,
        unit="mm",
        observed_at=observed_at,
        retrieved_at=retrieved_at,
        latitude=latitude,
        longitude=longitude,
        quality=quality,
        data_status=data_status,
    )


def open_meteo_rainfall_observations(
    latitude: float,
    longitude: float,
    *,
    start_date: str,
    end_date: str,
    source_id: str = "open-meteo-archive",
    base_url: str = "https://archive-api.open-meteo.com/v1/archive",
    model: str | None = None,
) -> list[Observation]:
    """Ingest Open-Meteo historical precipitation as explicitly MODELED evidence.

    Open-Meteo historical weather data is reanalysis/model output, not a site
    rain-gauge measurement. The adapter boundary therefore emits Observation
    records classified as MODELED so downstream DMRV cannot mistake them for
    physical telemetry. Hourly precipitation is the preceding-hour total.
    """
    from urllib.parse import urlencode

    params = {
        "latitude": str(latitude),
        "longitude": str(longitude),
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "precipitation",
        "timezone": "UTC",
    }
    if model:
        params["models"] = model

    payload = fetch_json(f"{base_url}?{urlencode(params)}")
    hourly = payload.get("hourly")
    if not isinstance(hourly, dict):
        raise ValueError("Open-Meteo response missing hourly data")
    times = hourly.get("time")
    values = hourly.get("precipitation")
    if not isinstance(times, list) or not isinstance(values, list):
        raise ValueError("Open-Meteo response missing hourly time/precipitation arrays")
    if len(times) != len(values):
        raise ValueError("Open-Meteo time and precipitation arrays must have equal length")

    retrieved_at = utc_now()
    observations: list[Observation] = []
    for observed_at, rainfall_mm in zip(times, values):
        if rainfall_mm is None:
            continue
        try:
            value = float(rainfall_mm)
        except (TypeError, ValueError) as exc:
            raise ValueError("Open-Meteo precipitation values must be numeric or null") from exc
        observations.append(
            rainfall_observation(
                source_id=source_id,
                provider="Open-Meteo",
                observed_at=str(observed_at),
                rainfall_mm=value,
                latitude=latitude,
                longitude=longitude,
                quality="SOURCE_VALIDATED",
                kind="REANALYSIS",
                data_status="MODELED",
            )
        )

    # Retrieval time is deliberately not part of the deterministic observation
    # ID, so the same source/time/value cannot silently become a new observation.
    # Each Observation retains its own ingestion timestamp for audit provenance.
    _ = retrieved_at
    return observations
