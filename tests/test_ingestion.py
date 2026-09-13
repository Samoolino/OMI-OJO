import json
import unittest
from unittest.mock import patch

from src.production.ingestion import (
    deterministic_id,
    open_meteo_forecast_snapshot,
    open_meteo_rainfall_observations,
    rainfall_observation,
)


class IngestionTests(unittest.TestCase):
    def test_deterministic_id(self):
        self.assertEqual(deterministic_id("x", "abc"), deterministic_id("x", "abc"))
        self.assertNotEqual(deterministic_id("x", "abc"), deterministic_id("x", "abd"))

    def test_rainfall_observation_is_provenance_bearing(self):
        observation = rainfall_observation(
            source_id="site-rain-gauge",
            provider="SITE_SENSOR",
            observed_at="2026-09-13T00:00:00Z",
            rainfall_mm=12.5,
            latitude=6.5244,
            longitude=3.3792,
        )
        self.assertEqual(observation.variable, "precipitation")
        self.assertEqual(observation.unit, "mm")
        self.assertEqual(observation.data_status, "MEASURED")
        self.assertEqual(len(observation.evidence_hash), 64)

    def test_negative_rainfall_rejected(self):
        with self.assertRaises(ValueError):
            rainfall_observation(
                source_id="site-rain-gauge",
                provider="SITE_SENSOR",
                observed_at="2026-09-13T00:00:00Z",
                rainfall_mm=-1,
            )

    @patch("src.production.ingestion.fetch_json")
    def test_forecast_snapshot_is_immutable_and_hashed(self, fetch):
        fetch.return_value = {"hourly": {"time": ["2026-09-13T00:00:00Z"], "precipitation": [2.0]}}
        first = open_meteo_forecast_snapshot(6.5244, 3.3792)
        second = open_meteo_forecast_snapshot(6.5244, 3.3792)
        self.assertEqual(first.payload, second.payload)
        self.assertNotEqual(first.snapshot_id, second.snapshot_id)
        self.assertEqual(len(first.evidence_hash), 64)
        json.dumps(first.payload)

    @patch("src.production.ingestion.fetch_json")
    def test_open_meteo_rainfall_is_explicitly_modeled(self, fetch):
        fetch.return_value = {
            "hourly": {
                "time": ["2026-09-12T23:00:00Z", "2026-09-13T00:00:00Z"],
                "precipitation": [3.2, 0.0],
            }
        }
        observations = open_meteo_rainfall_observations(
            6.5244,
            3.3792,
            start_date="2026-09-12",
            end_date="2026-09-13",
        )
        self.assertEqual(len(observations), 2)
        self.assertEqual(observations[0].provider, "Open-Meteo")
        self.assertEqual(observations[0].kind, "REANALYSIS")
        self.assertEqual(observations[0].data_status, "MODELED")
        self.assertEqual(observations[0].value, 3.2)
        self.assertEqual(observations[1].value, 0.0)
        self.assertEqual(len(observations[0].evidence_hash), 64)

    @patch("src.production.ingestion.fetch_json")
    def test_open_meteo_rejects_misaligned_arrays(self, fetch):
        fetch.return_value = {
            "hourly": {
                "time": ["2026-09-13T00:00:00Z"],
                "precipitation": [1.0, 2.0],
            }
        }
        with self.assertRaises(ValueError):
            open_meteo_rainfall_observations(
                6.5244,
                3.3792,
                start_date="2026-09-13",
                end_date="2026-09-13",
            )


if __name__ == "__main__":
    unittest.main()
