# Informatica and Governance Extension

This project keeps Informatica as an enterprise-grade integration layer rather than a toy local dependency.

## Suggested IICS Taskflows

- SAP order header and line-item CDC into S3 Bronze.
- CRM customer profile snapshots into S3 Bronze.
- Payment processor reconciliation files into Snowflake RAW.
- Metadata publication to OpenMetadata or DataHub.

## Integration Pattern

1. Informatica extracts enterprise data sources using CDC or scheduled ingestion.
2. Raw records land in S3 using the same Bronze partitioning standard as streaming events.
3. Databricks joins enterprise CDC data with clickstream and order events.
4. dbt owns conformed dimensions and facts in Snowflake.
5. OpenMetadata captures lineage, ownership, freshness, and data quality status.

## Interview Framing

The important point is not that every service runs locally. The important point is that the architecture cleanly separates:

- operational event ingestion
- enterprise source ingestion
- raw data retention
- lakehouse processing
- warehouse modeling
- governance and observability

