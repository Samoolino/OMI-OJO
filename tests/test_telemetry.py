import unittest

from src.production.telemetry import ingest_measured_rainfall_record, ingest_measured_rainfall_records


class MeasuredTelemetryTests(unittest.TestCase):
    def test_normalizes_measured_station_record(self) -> None:
        observation = ingest_measured_rainfall_record(
            {
                "observed_at": "2026-09-13T00:00:00Z",
                "rainfall_mm": 12.5,
                "quality": "DEVICE_VALIDATED",
            },
            source_id="site-rain-gauge",
            provider="Site Gauge",
            latitude=6.52,
            longitude=3.38,
        )
        self.assertEqual(observation.data_status, "MEASURED")
        self.assertEqual(observation.variable, "precipitation")
        self.assertEqual(observation.value, 12.5)
        self.assertEqual(observation.latitude, 6.52)
        self.assertEqual(observation.longitude, 3.38)
        self.assertTrue(observation.evidence_hash)

    def test_rejects_non_measured_classification(self) -> None:
        with self.assertRaises(ValueError):
            ingest_measured_rainfall_record(
                {
                    "observed_at": "2026-09-13T00:00:00Z",
                    "rainfall_mm": 1,
                    "data_status": "FORECAST",
                },
                source_id="site-rain-gauge",
                provider="Site Gauge",
            )

    def test_rejects_missing_timestamp(self) -> None:
        with self.assertRaises(ValueError):
            ingest_measured_rainfall_record(
                {"rainfall_mm": 1},
                source_id="site-rain-gauge",
                provider="Site Gauge",
            )

    def test_batch_preserves_distinct_observation_identity(self) -> None:
        observations = ingest_measured_rainfall_records(
            [
                {"observed_at": "2026-09-13T00:00:00Z", "rainfall_mm": 1},
                {"observed_at": "2026-09-13T01:00:00Z", "rainfall_mm": 2},
            ],
            source_id="site-rain-gauge",
            provider="Site Gauge",
        )
        self.assertEqual(len(observations), 2)
        self.assertNotEqual(observations[0].observation_id, observations[1].observation_id)


if __name__ == "__main__":
    unittest.main()
