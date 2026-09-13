import json
import unittest
from unittest.mock import patch

from src.production.ingestion import (
    Observation,
    deterministic_id,
    open_meteo_forecast_snapshot,
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


if __name__ == "__main__":
    unittest.main()
