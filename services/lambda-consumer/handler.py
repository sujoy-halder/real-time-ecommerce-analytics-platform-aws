from __future__ import annotations

import base64
import json
import os
from datetime import UTC, datetime
from typing import Any

import boto3


AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL") or None
BRONZE_BUCKET = os.environ.get("BRONZE_BUCKET", "ecommerce-bronze-dev")


def _partition_key(event: dict[str, Any], ingest_time: datetime) -> str:
    event_type = str(event.get("event_type", "unknown")).replace("/", "_")
    event_id = str(event.get("event_id", "missing-event-id")).replace("/", "_")
    return (
        f"events/event_type={event_type}/"
        f"ingest_date={ingest_time:%Y-%m-%d}/"
        f"hour={ingest_time:%H}/"
        f"{event_id}.json"
    )


def _decode_record(record: dict[str, Any]) -> dict[str, Any]:
    raw_payload = base64.b64decode(record["kinesis"]["data"]).decode("utf-8")
    return json.loads(raw_payload)


def _s3_client() -> Any:
    kwargs = {
        "region_name": AWS_REGION,
        "endpoint_url": AWS_ENDPOINT_URL,
    }
    if AWS_ENDPOINT_URL:
        kwargs["aws_access_key_id"] = os.getenv("AWS_ACCESS_KEY_ID", "test")
        kwargs["aws_secret_access_key"] = os.getenv("AWS_SECRET_ACCESS_KEY", "test")
    return boto3.client("s3", **kwargs)


def _put_event_to_bronze(
    s3_client: Any,
    event: dict[str, Any],
    sequence_number: str,
    ingest_time: datetime,
) -> None:
    key = _partition_key(event, ingest_time)
    s3_client.put_object(
        Bucket=BRONZE_BUCKET,
        Key=key,
        Body=json.dumps(event, separators=(",", ":")).encode("utf-8"),
        ContentType="application/json",
        Metadata={
            "event-type": str(event.get("event_type", "unknown")),
            "source-sequence-number": sequence_number,
        },
    )


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    batch_failures = []
    ingest_time = datetime.now(UTC)
    s3_client = _s3_client()

    for record in event.get("Records", []):
        sequence_number = record["kinesis"]["sequenceNumber"]
        try:
            decoded = _decode_record(record)
            _put_event_to_bronze(s3_client, decoded, sequence_number, ingest_time)
        except Exception:
            batch_failures.append({"itemIdentifier": sequence_number})

    return {"batchItemFailures": batch_failures}
