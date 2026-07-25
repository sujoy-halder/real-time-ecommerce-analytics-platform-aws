from __future__ import annotations

import base64
import importlib.util
import json
import os
import sys
import types
import unittest
from datetime import UTC, datetime
from pathlib import Path


class LambdaConsumerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.environ["BRONZE_BUCKET"] = "bronze-test"
        os.environ["AWS_EC2_METADATA_DISABLED"] = "true"
        sys.modules["boto3"] = types.SimpleNamespace(client=lambda service_name: object())

        handler_path = Path(__file__).resolve().parents[1] / "handler.py"
        spec = importlib.util.spec_from_file_location("lambda_consumer_handler", handler_path)
        if spec is None or spec.loader is None:
            raise RuntimeError("Unable to load Lambda handler module")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        cls.handler_module = module

    def test_decodes_kinesis_payload(self) -> None:
        payload = {"event_id": "evt-1", "event_type": "order_created"}
        record = {
            "kinesis": {
                "data": base64.b64encode(json.dumps(payload).encode("utf-8")).decode("utf-8")
            }
        }

        decoded = self.handler_module._decode_record(record)

        self.assertEqual(decoded, payload)

    def test_partition_key_uses_event_type_date_hour_and_event_id(self) -> None:
        event = {"event_id": "evt-1", "event_type": "order_created"}
        ingest_time = datetime(2026, 7, 16, 14, 30, tzinfo=UTC)

        key = self.handler_module._partition_key(event, ingest_time)

        self.assertEqual(
            key,
            "events/event_type=order_created/ingest_date=2026-07-16/hour=14/evt-1.json",
        )


if __name__ == "__main__":
    unittest.main()

