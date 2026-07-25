from __future__ import annotations

import json
import time
from typing import Any

from app.config import ProducerConfig


class KinesisPublisher:
    def __init__(self, config: ProducerConfig) -> None:
        try:
            import boto3
        except ImportError as exc:
            raise RuntimeError("boto3 is required to publish events to Kinesis") from exc

        self.stream_name = config.stream_name
        self.stream_shard_count = config.stream_shard_count
        self.client = boto3.client(
            "kinesis",
            region_name=config.aws_region,
            endpoint_url=config.aws_endpoint_url,
        )
        if config.auto_create_stream:
            self._ensure_stream()

    def publish_batch(self, events: list[dict[str, Any]]) -> dict[str, Any]:
        records = [
            {
                "Data": json.dumps(event, separators=(",", ":")).encode("utf-8"),
                "PartitionKey": event["customer_id"],
            }
            for event in events
        ]
        return self.client.put_records(StreamName=self.stream_name, Records=records)

    def _ensure_stream(self) -> None:
        try:
            self.client.describe_stream_summary(StreamName=self.stream_name)
        except self.client.exceptions.ResourceNotFoundException:
            self.client.create_stream(
                StreamName=self.stream_name,
                ShardCount=self.stream_shard_count,
            )

        deadline = time.monotonic() + 60
        while time.monotonic() < deadline:
            response = self.client.describe_stream_summary(StreamName=self.stream_name)
            status = response["StreamDescriptionSummary"]["StreamStatus"]
            if status == "ACTIVE":
                return
            time.sleep(2)

        raise TimeoutError(f"Kinesis stream did not become ACTIVE: {self.stream_name}")
