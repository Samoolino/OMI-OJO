import unittest

from src.production.event_engine import activate_event, append_measurement, complete_event, detect_event
from src.production.ingestion import rainfall_observation


class RainfallEventEngineTests(unittest.TestCase):
    def _obs(self, hour: str, value: float):
        return rainfall_observation(
            source_id="site-rain-gauge",
            provider="Site Gauge",
            observed_at=f"2026-09-13T{hour}:00:00Z",
            rainfall_mm=value,
            quality="DEVICE_VALIDATED",
        )

    def test_measured_observation_advances_event(self) -> None:
        first = self._obs("01", 4.0)
        event = detect_event(first)
        self.assertEqual(event.status.value, "RAIN_EVENT_DETECTED")
        event = activate_event(event)
        event = append_measurement(event, self._obs("02", 3.0))
        event = complete_event(event)
        self.assertEqual(event.status.value, "RAIN_EVENT_COMPLETE")
        self.assertEqual(event.cumulative_mm, 7.0)
        self.assertEqual(len(event.observation_ids), 2)

    def test_non_measured_data_cannot_start_event(self) -> None:
        observation = rainfall_observation(
            source_id="open-meteo-archive",
            provider="Open-Meteo",
            observed_at="2026-09-13T01:00:00Z",
            rainfall_mm=4,
            kind="REANALYSIS",
            data_status="MODELED",
        )
        with self.assertRaises(ValueError):
            detect_event(observation)


if __name__ == "__main__":
    unittest.main()
