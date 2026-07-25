from __future__ import annotations

import os

import boto3
from botocore.exceptions import ClientError


AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566")
STREAM_NAME = os.getenv("KINESIS_STREAM_NAME", "ecommerce-events-dev")
BUCKET_NAME = os.getenv("BRONZE_BUCKET", "ecommerce-bronze-dev")


def ensure_stream() -> None:
    kinesis = boto3.client("kinesis", region_name=AWS_REGION, endpoint_url=ENDPOINT_URL)
    try:
        kinesis.describe_stream_summary(StreamName=STREAM_NAME)
        print(f"Kinesis stream already exists: {STREAM_NAME}")
    except ClientError as exc:
        if exc.response["Error"]["Code"] != "ResourceNotFoundException":
            raise
        kinesis.create_stream(StreamName=STREAM_NAME, ShardCount=2)
        print(f"Created Kinesis stream: {STREAM_NAME}")


def ensure_bucket() -> None:
    s3 = boto3.client("s3", region_name=AWS_REGION, endpoint_url=ENDPOINT_URL)
    try:
        s3.head_bucket(Bucket=BUCKET_NAME)
        print(f"S3 bucket already exists: {BUCKET_NAME}")
    except ClientError:
        s3.create_bucket(Bucket=BUCKET_NAME)
        print(f"Created S3 bucket: {BUCKET_NAME}")


if __name__ == "__main__":
    ensure_stream()
    ensure_bucket()

