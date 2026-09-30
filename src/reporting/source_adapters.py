"""Canonical source-adapter boundary for Climate & ESG ingestion.

Adapters translate provider payloads into the reporting domain. They do not
decide release status and they never upgrade evidence classes.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping, Sequence

from src.production.ingestion import open_meteo_forecast_snapshot
from .reportable_data import EvidenceClass, Location, Observation


@dataclass(frozen=True)
class SourceRequest:
    project_id: str
    site_id: str
    indicator_ids: tuple[str, ...]
    location: Location
    source_id: str


class SourceAdapter(ABC):
    source_id: str

    @abstractmethod
    def ingest(self, request: SourceRequest) -> Sequence[Observation]:
        """Return canonical observations only; no release decision is made."""


class OpenMeteoForecastAdapter(SourceAdapter):
    source_id = "open-meteo-forecast"

    def __init__(self, base_url: str = "https://api.open-meteo.com/v1/forecast") -> None:
        self.base_url = base_url

    def ingest(self, request: SourceRequest) -> Sequence[Observation]:
        if request.source_id != self.source_id:
            raise ValueError(f"adapter/source mismatch: {request.source_id}")
        snapshot = open_meteo_forecast_snapshot(
            request.location.latitude,
            request.location.longitude,
            source_id=self.source_id,
            base_url=self.base_url,
        )
        hourly = snapshot.payload.get("hourly")
        if not isinstance(hourly, Mapping):
            raise ValueError("Open-Meteo forecast response missing hourly data")
        times = hourly.get("time")
        if not isinstance(times, list):
            raise ValueError("Open-Meteo forecast response missing hourly time")

        variable_map: dict[str, tuple[str, str]] = {
            "rainfall": ("precipitation", "mm"),
            "temperature": ("temperature_2m", "°C"),
            "relative_humidity": ("relative_humidity_2m", "%"),
            "pressure": ("pressure_msl", "hPa"),
            "wind_speed": ("wind_speed_10m", "km/h"),
        }
        result: list[Observation] = []
        for indicator_id in request.indicator_ids:
            spec = variable_map.get(indicator_id)
            if spec is None:
                continue
            variable, unit = spec
            values = hourly.get(variable)
            if not isinstance(values, list) or len(values) != len(times):
                raise ValueError(f"Open-Meteo response missing aligned {variable} values")
            for observed_at, value in zip(times, values):
                if value is None:
                    continue
                dt = datetime.fromisoformat(str(observed_at).replace("Z", "+00:00"))
                canonical_seed = f"{request.project_id}|{request.site_id}|{indicator_id}|{dt.isoformat()}|{self.source_id}"
                import hashlib
                observation_id = "ro_" + hashlib.sha256(canonical_seed.encode()).hexdigest()[:24]
                result.append(
                    Observation(
                        observation_id=observation_id,
                        project_id=request.project_id,
                        site_id=request.site_id,
                        indicator_id=indicator_id,
                        observed_at=dt.astimezone(timezone.utc),
                        location=request.location,
                        value=float(value),
                        unit=unit,
                        source_id=self.source_id,
                        evidence_class=EvidenceClass.MODELED,
                        qc_passed=True,
                        reconciled=False,
                        metadata={
                            "provider": "Open-Meteo",
                            "source_snapshot_id": snapshot.snapshot_id,
                            "methodology_status": "REMOTE_CONTEXT_ONLY",
                            "physical_claim_allowed": "false",
                        },
                    )
                )
        return result


def adapter_for(source_id: str, *, base_url: str | None = None) -> SourceAdapter:
    """Resolve an approved adapter without allowing unknown provider fallbacks."""
    if source_id == OpenMeteoForecastAdapter.source_id:
        return OpenMeteoForecastAdapter(base_url=base_url or "https://api.open-meteo.com/v1/forecast")
    raise ValueError(f"no approved adapter registered for source: {source_id}")
