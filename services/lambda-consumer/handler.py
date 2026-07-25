from __future__ import annotations

import base64
import json
import os
from datetime import UTC, datetime
from typing import Any

import boto3


s3 = boto3.client("s3")
BRONZE_BUCKET = os.environ["BRONZE_BUCKET"]


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


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    batch_failures = []
    ingest_time = datetime.now(UTC)

    for record in event.get("Records", []):
        sequence_number = record["kinesis"]["sequenceNumber"]
        try:
            decoded = _decode_record(record)
            key = _partition_key(decoded, ingest_time)
            s3.put_object(
                Bucket=BRONZE_BUCKET,
                Key=key,
                Body=json.dumps(decoded, separators=(",", ":")).encode("utf-8"),
                ContentType="application/json",
                Metadata={
                    "event-type": str(decoded.get("event_type", "unknown")),
                    "source-sequence-number": sequence_number,
                },
            )
        except Exception:
            batch_failures.append({"itemIdentifier": sequence_number})

    return {"batchItemFailures": batch_failures}

