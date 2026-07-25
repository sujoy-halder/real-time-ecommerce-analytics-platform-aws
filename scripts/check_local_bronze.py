from __future__ import annotations

import os

import boto3


AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566") or None
BUCKET_NAME = os.getenv("BRONZE_BUCKET", "ecommerce-bronze-dev")


def s3_client():
    kwargs = {
        "region_name": AWS_REGION,
        "endpoint_url": ENDPOINT_URL,
    }
    if ENDPOINT_URL:
        kwargs["aws_access_key_id"] = os.getenv("AWS_ACCESS_KEY_ID", "test")
        kwargs["aws_secret_access_key"] = os.getenv("AWS_SECRET_ACCESS_KEY", "test")
    return boto3.client("s3", **kwargs)


def main() -> int:
    response = s3_client().list_objects_v2(Bucket=BUCKET_NAME, Prefix="events/")
    objects = response.get("Contents", [])
    print(f"bronze_bucket={BUCKET_NAME}")
    print(f"event_objects={len(objects)}")
    for item in objects[:10]:
        print(item["Key"])
    return 0 if objects else 1


if __name__ == "__main__":
    raise SystemExit(main())

