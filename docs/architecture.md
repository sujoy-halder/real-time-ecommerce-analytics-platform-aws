# Architecture Notes

## Event Ingestion

Producer services run as horizontally scaled Kubernetes deployments on EKS. Each replica generates domain events and writes them to Amazon Kinesis. Partition keys use stable business identifiers such as `customer_id` and `order_id` so related events remain ordered where it matters.

## Bronze Layer

A Lambda consumer reads Kinesis batches and stores immutable JSON in S3 using partitioned paths:

```text
s3://<bronze-bucket>/events/event_type=<type>/ingest_date=YYYY-MM-DD/hour=HH/<event_id>.json
```

This gives the platform replayability, auditability, and a clean contract between ingestion and processing.

## Databricks Lakehouse

Databricks reads Bronze data with Structured Streaming. The notebook included here shows:

- schema parsing
- bad-record isolation
- event deduplication by `event_id`
- event-time watermarking
- sessionization for clickstream and customer activity
- Delta Bronze, Silver, and Gold table writes

## Snowflake and dbt

Gold tables are copied into Snowflake for analytics serving. dbt owns the dimensional model:

- `fact_orders`
- `fact_payments`
- `dim_customers`
- `dim_products`

The dbt layer includes uniqueness, not-null, accepted-values, and relationship tests.

## Enterprise Extensions

Informatica IICS can provide governed ingestion for SAP, CRM, ERP, and CDC feeds that join with e-commerce telemetry. OpenMetadata or DataHub can index table lineage, owners, freshness, and quality checks.

## Reliability

The design uses:

- Kinesis retention for replay windows
- Lambda partial batch failure handling
- S3 raw retention policies
- Kubernetes HPA for producers and APIs
- CloudWatch alarms for iterator age, Lambda errors, and stream throughput
- dbt and Great Expectations quality gates in CI/CD

