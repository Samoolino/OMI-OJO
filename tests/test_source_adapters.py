from datetime import datetime, timezone
import json

from src.reporting.reportable_data import EvidenceClass, Location
from src.reporting.source_adapters import OpenMeteoForecastAdapter, SourceRequest


def test_open_meteo_adapter_maps_without_promoting_evidence(monkeypatch):
    payload = {
        "hourly": {
            "time": ["2026-09-30T00:00", "2026-09-30T01:00"],
            "precipitation": [1.2, 0.0],
            "temperature_2m": [25.0, 25.5],
            "relative_humidity_2m": [80, 78],
            "pressure_msl": [1010, 1011],
            "wind_speed_10m": [10, 12],
        }
    }

    class Response:
        status = 200
        def read(self):
            return json.dumps(payload).encode()

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

    monkeypatch.setattr("src.production.ingestion.urlopen", lambda *args, **kwargs: Response())

    observations = OpenMeteoForecastAdapter().ingest(
        SourceRequest(
            project_id="S5-GLOBAL-LAGOS",
            site_id="lagos-reference-grid",
            indicator_ids=("rainfall", "temperature"),
            location=Location(6.5, 3.4),
            source_id="open-meteo-forecast",
        )
    )

    assert len(observations) == 4
    assert all(o.evidence_class is EvidenceClass.MODELED for o in observations)
    assert all(o.metadata["physical_claim_allowed"] == "false" for o in observations)
    assert observations[0].source_id == "open-meteo-forecast"


def test_unknown_source_is_rejected():
    from src.reporting.source_adapters import adapter_for
    try:
        adapter_for("unregistered-provider")
    except ValueError as exc:
        assert "no approved adapter" in str(exc)
    else:
        raise AssertionError("unknown source must not fall back to an adapter")
