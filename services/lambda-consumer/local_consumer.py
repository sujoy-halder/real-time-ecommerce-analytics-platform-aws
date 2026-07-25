from __future__ import annotations

import json
import os
import time
from datetime import UTC, datetime
from typing import Any

import boto3
from botocore.exceptions import ClientError

from handler import BRONZE_BUCKET, _put_event_to_bronze


AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL") or None
STREAM_NAME = os.getenv("KINESIS_STREAM_NAME", "ecommerce-events-dev")
SHARD_COUNT = int(os.getenv("KINESIS_SHARD_COUNT", "2"))
POLL_SECONDS = float(os.getenv("CONSUMER_POLL_SECONDS", "1.0"))
AUTO_CREATE_STREAM = os.getenv("AUTO_CREATE_STREAM", "true").lower() == "true"
AUTO_CREATE_BUCKET = os.getenv("AUTO_CREATE_BUCKET", "true").lower() == "true"


def _client(service_name: str) -> Any:
    kwargs = {
        "region_name": AWS_REGION,
        "endpoint_url": AWS_ENDPOINT_URL,
    }
    if AWS_ENDPOINT_URL:
        kwargs["aws_access_key_id"] = os.getenv("AWS_ACCESS_KEY_ID", "test")
        kwargs["aws_secret_access_key"] = os.getenv("AWS_SECRET_ACCESS_KEY", "test")
    return boto3.client(service_name, **kwargs)


def _wait_for_stream(kinesis: Any) -> None:
    deadline = time.monotonic() + 60
    while time.monotonic() < deadline:
        response = kinesis.describe_stream_summary(StreamName=STREAM_NAME)
        status = response["StreamDescriptionSummary"]["StreamStatus"]
        if status == "ACTIVE":
            return
        time.sleep(2)
    raise TimeoutError(f"Kinesis stream did not become ACTIVE: {STREAM_NAME}")


def ensure_stream(kinesis: Any) -> None:
    try:
        kinesis.describe_stream_summary(StreamName=STREAM_NAME)
    except kinesis.exceptions.ResourceNotFoundException:
        if not AUTO_CREATE_STREAM:
            raise
        try:
            kinesis.create_stream(StreamName=STREAM_NAME, ShardCount=SHARD_COUNT)
        except kinesis.exceptions.ResourceInUseException:
            pass
    _wait_for_stream(kinesis)


def ensure_bucket(s3_client: Any) -> None:
    try:
        s3_client.head_bucket(Bucket=BRONZE_BUCKET)
    except ClientError:
        if not AUTO_CREATE_BUCKET:
            raise
        s3_client.create_bucket(Bucket=BRONZE_BUCKET)


def shard_iterators(kinesis: Any) -> dict[str, str]:
    iterators = {}
    paginator = kinesis.get_paginator("list_shards")
    for page in paginator.paginate(StreamName=STREAM_NAME):
        for shard in page["Shards"]:
            shard_id = shard["ShardId"]
            response = kinesis.get_shard_iterator(
                StreamName=STREAM_NAME,
                ShardId=shard_id,
                ShardIteratorType="TRIM_HORIZON",
            )
            iterators[shard_id] = response["ShardIterator"]
    return iterators


def consume_forever() -> None:
    kinesis = _client("kinesis")
    s3_client = _client("s3")
    ensure_stream(kinesis)
    ensure_bucket(s3_client)
    iterators = shard_iterators(kinesis)

    print(
        json.dumps(
            {
                "message": "local_consumer_started",
                "stream": STREAM_NAME,
                "bronze_bucket": BRONZE_BUCKET,
                "shards": len(iterators),
            }
        ),
        flush=True,
    )

    while True:
        for shard_id, iterator in list(iterators.items()):
            response = kinesis.get_records(ShardIterator=iterator, Limit=100)
            iterators[shard_id] = response["NextShardIterator"]

            for record in response["Records"]:
                event = json.loads(record["Data"].decode("utf-8"))
                _put_event_to_bronze(
                    s3_client,
                    event,
                    record["SequenceNumber"],
                    datetime.now(UTC),
                )

            if response["Records"]:
                print(
                    json.dumps(
                        {
                            "message": "wrote_events_to_bronze",
                            "records": len(response["Records"]),
                            "shard_id": shard_id,
                        }
                    ),
                    flush=True,
                )

        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    consume_forever()
