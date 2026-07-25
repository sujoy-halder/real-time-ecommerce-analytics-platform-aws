from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ProducerConfig:
    stream_name: str
    aws_region: str
    aws_endpoint_url: str | None
    interval_seconds: float
    batch_size: int
    mode: str
    auto_create_stream: bool
    stream_shard_count: int

    @classmethod
    def from_env(cls) -> "ProducerConfig":
        return cls(
            stream_name=os.getenv("KINESIS_STREAM_NAME", "ecommerce-events-dev"),
            aws_region=os.getenv("AWS_REGION", "us-east-1"),
            aws_endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
            interval_seconds=float(os.getenv("PRODUCER_INTERVAL_SECONDS", "1.0")),
            batch_size=int(os.getenv("PRODUCER_BATCH_SIZE", "10")),
            mode=os.getenv("PRODUCER_MODE", "continuous"),
            auto_create_stream=os.getenv("AUTO_CREATE_STREAM", "false").lower() == "true",
            stream_shard_count=int(os.getenv("KINESIS_SHARD_COUNT", "2")),
        )
