"""Measured telemetry adapter boundary for physical rain-gauge evidence.

The adapter accepts operator/device payloads and converts them into the same
immutable Observation contract used by DMRV reconciliation. It never infers
measurement status from a forecast source and rejects ambiguous records.
"""
from __future__ import annotations

from typing import Any, Iterable

from .ingestion import Observation, rainfall_observation


REQUIRED_FIELDS = ("observed_at", "rainfall_mm")


def ingest_measured_rainfall_record(
    record: dict[str, Any],
    *,
    source_id: str,
    provider: str,
    latitude: float | None = None,
    longitude: float | None = None,
    quality: str = "UNASSESSED",
    kind: str = "STATION",
) -> Observation:
    """Normalize one physical rain-gauge record as MEASURED evidence.

    The caller is responsible for the device/source registry asserting that the
    source is an approved measurement device. This function deliberately does
    not upgrade arbitrary data to verified status.
    """
    if not isinstance(record, dict):
        raise TypeError("telemetry record must be an object")
    missing = [field for field in REQUIRED_FIELDS if field not in record]
    if missing:
        raise ValueError(f"telemetry record missing required fields: {', '.join(missing)}")

    observed_at = record["observed_at"]
    if not isinstance(observed_at, str) or not observed_at.strip():
        raise ValueError("observed_at must be a non-empty ISO timestamp string")

    try:
        rainfall_mm = float(record["rainfall_mm"])
    except (TypeError, ValueError) as exc:
        raise ValueError("rainfall_mm must be numeric") from exc

    if record.get("data_status", "MEASURED") != "MEASURED":
        raise ValueError("measured telemetry adapter only accepts data_status=MEASURED")

    return rainfall_observation(
        source_id=source_id,
        provider=provider,
        observed_at=observed_at,
        rainfall_mm=rainfall_mm,
        latitude=latitude if latitude is not None else _optional_float(record.get("latitude")),
        longitude=longitude if longitude is not None else _optional_float(record.get("longitude")),
        quality=str(record.get("quality", quality)),
        kind=str(record.get("kind", kind)),
        data_status="MEASURED",
    )


def ingest_measured_rainfall_records(
    records: Iterable[dict[str, Any]],
    *,
    source_id: str,
    provider: str,
    latitude: float | None = None,
    longitude: float | None = None,
    quality: str = "UNASSESSED",
) -> list[Observation]:
    """Normalize an ordered collection while preserving per-record identity."""
    return [
        ingest_measured_rainfall_record(
            record,
            source_id=source_id,
            provider=provider,
            latitude=latitude,
            longitude=longitude,
            quality=quality,
        )
        for record in records
    ]


def _optional_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("latitude/longitude must be numeric when provided") from exc
