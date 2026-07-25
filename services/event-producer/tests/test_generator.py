from __future__ import annotations

import random
import unittest
from datetime import UTC, datetime

from app.generator import EVENT_TYPES, generate_batch, generate_event


class EventGeneratorTests(unittest.TestCase):
    def test_generates_supported_event_types(self) -> None:
        for event_type in EVENT_TYPES:
            event = generate_event(
                event_type,
                rng=random.Random(7),
                clock=lambda: datetime(2026, 7, 16, 12, 0, tzinfo=UTC),
            )
            self.assertEqual(event["event_type"], event_type)
            self.assertEqual(event["event_time"], "2026-07-16T12:00:00Z")
            self.assertIn("event_id", event)
            self.assertIn("customer_id", event)
            self.assertIsInstance(event["payload"], dict)

    def test_batch_size_must_be_positive(self) -> None:
        with self.assertRaises(ValueError):
            generate_batch(0)

    def test_batch_contains_requested_number_of_events(self) -> None:
        batch = generate_batch(25, rng=random.Random(11))
        self.assertEqual(len(batch), 25)


if __name__ == "__main__":
    unittest.main()

