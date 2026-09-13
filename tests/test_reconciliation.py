import unittest

from src.production.ingestion import open_meteo_forecast_snapshot, rainfall_observation
from src.production.reconciliation import compare_forecast_to_measurement, summarize_accuracy
from unittest.mock import patch


class ReconciliationTests(unittest.TestCase):
    @patch("src.production.ingestion.fetch_json")
    def test_forecast_is_reconciled_only_against_measured_telemetry(self, fetch):
        timestamp = "2026-09-13T01:00:00Z"
        fetch.return_value = {
            "hourly": {"time": [timestamp], "precipitation": [10.0]}
        }
        snapshot = open_meteo_forecast_snapshot(6.5244, 3.3792)
        observation = rainfall_observation(
            source_id="site-rain-gauge",
            provider="SITE_SENSOR",
            observed_at=timestamp,
            rainfall_mm=8.0,
            latitude=6.5244,
            longitude=3.3792,
        )
        result = compare_forecast_to_measurement(snapshot, observation)
        self.assertEqual(result.forecast_mm, 10.0)
        self.assertEqual(result.measured_mm, 8.0)
        self.assertEqual(result.comparison.absolute_error_mm, 2.0)
        self.assertEqual(result.accuracy_percent, 75.0)

    @patch("src.production.ingestion.fetch_json")
    def test_summary_is_deterministic_for_comparison_set(self, fetch):
        timestamp = "2026-09-13T01:00:00Z"
        fetch.return_value = {"hourly": {"time": [timestamp], "precipitation": [10.0]}}
        snapshot = open_meteo_forecast_snapshot(6.5244, 3.3792)
        observation = rainfall_observation(
            source_id="site-rain-gauge", provider="SITE_SENSOR",
            observed_at=timestamp, rainfall_mm=10.0,
        )
        comparison = compare_forecast_to_measurement(snapshot, observation)
        summary = summarize_accuracy([comparison])
        self.assertEqual(summary["sample_count"], 1)
        self.assertEqual(summary["mean_accuracy_percent"], 100.0)
        self.assertEqual(summary["mean_absolute_error_mm"], 0.0)


if __name__ == "__main__":
    unittest.main()
