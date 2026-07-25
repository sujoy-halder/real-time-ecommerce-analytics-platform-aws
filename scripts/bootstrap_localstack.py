from __future__ import annotations

import os

import boto3
from botocore.exceptions import ClientError


AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566") or None
STREAM_NAME = os.getenv("KINESIS_STREAM_NAME", "ecommerce-events-dev")
BUCKET_NAME = os.getenv("BRONZE_BUCKET", "ecommerce-bronze-dev")


def client(service_name: str):
    kwargs = {
        "region_name": AWS_REGION,
        "endpoint_url": ENDPOINT_URL,
    }
    if ENDPOINT_URL:
        kwargs["aws_access_key_id"] = os.getenv("AWS_ACCESS_KEY_ID", "test")
        kwargs["aws_secret_access_key"] = os.getenv("AWS_SECRET_ACCESS_KEY", "test")
    return boto3.client(service_name, **kwargs)


def ensure_stream() -> None:
    kinesis = client("kinesis")
    try:
        kinesis.describe_stream_summary(StreamName=STREAM_NAME)
        print(f"Kinesis stream already exists: {STREAM_NAME}")
    except ClientError as exc:
        if exc.response["Error"]["Code"] != "ResourceNotFoundException":
            raise
        kinesis.create_stream(StreamName=STREAM_NAME, ShardCount=2)
        print(f"Created Kinesis stream: {STREAM_NAME}")


def ensure_bucket() -> None:
    s3 = client("s3")
    try:
        s3.head_bucket(Bucket=BUCKET_NAME)
        print(f"S3 bucket already exists: {BUCKET_NAME}")
    except ClientError:
        create_kwargs = {"Bucket": BUCKET_NAME}
        if AWS_REGION != "us-east-1":
            create_kwargs["CreateBucketConfiguration"] = {
                "LocationConstraint": AWS_REGION,
            }
        s3.create_bucket(**create_kwargs)
        print(f"Created S3 bucket: {BUCKET_NAME}")


if __name__ == "__main__":
    ensure_stream()
    ensure_bucket()
