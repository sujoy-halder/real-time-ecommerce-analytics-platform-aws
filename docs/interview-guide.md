# Interview Guide

## Two-Minute Pitch

This project is a real-time e-commerce analytics platform. Python producer services emit orders, clicks, payments, sessions, and shipment events into Kinesis. A Lambda consumer writes immutable raw records into S3 Bronze. Databricks performs streaming ETL, deduplication, schema validation, CDC enrichment, sessionization, and Delta Lake table management. Curated Gold datasets are loaded to Snowflake, where dbt builds facts, dimensions, tests, docs, and lineage. Terraform, Docker, Helm, Kubernetes, GitHub Actions, CloudWatch, Great Expectations, and OpenMetadata make the platform production-shaped.

## Design Decisions

- Kinesis provides managed streaming ingestion with shard-based scaling and replay retention.
- S3 Bronze keeps raw events immutable, which makes reprocessing and audits possible.
- Databricks handles high-volume streaming transformations better than pushing all logic into Lambda.
- Delta Lake gives ACID writes, schema enforcement, and incremental processing.
- Snowflake serves curated analytics workloads independently from streaming compute.
- dbt owns business logic, dimensional modeling, tests, and documentation.
- Informatica is positioned for enterprise CDC and governed ingestion from SAP, CRM, and ERP systems.
- EKS and Helm show container orchestration and autoscaling for producer/API workloads.

## What To Demo

1. Run `docker compose up --build`.
2. Run `python scripts/bootstrap_localstack.py`.
3. Show producer logs publishing event batches to Kinesis.
4. Walk through the Lambda consumer and S3 Bronze partition strategy.
5. Open the Databricks notebook and explain Bronze, Silver, and Gold.
6. Open dbt models and show facts, dimensions, tests, and lineage.
7. Open Terraform modules and explain how infrastructure is separated by concern.
8. Open the GitHub Actions workflow and explain validation, image build, and deployment stages.

## Strong Resume Bullets

- Built a real-time e-commerce analytics platform using AWS Kinesis, Lambda, S3, Databricks, Snowflake, and dbt to process high-volume order, clickstream, payment, and session events.
- Designed a Bronze/Silver/Gold lakehouse with Delta Lake, streaming deduplication, schema validation, event-time processing, and curated Snowflake marts.
- Deployed Dockerized Python services to Kubernetes with Helm, Horizontal Pod Autoscaling, ConfigMaps, Secrets, and CI/CD through GitHub Actions.
- Implemented production-grade data quality and observability patterns using dbt tests, Great Expectations, CloudWatch alarms, and metadata ingestion.

## Follow-Up Enhancements

- Add a Debezium source connector for CDC from PostgreSQL order tables.
- Add Prometheus and Grafana dashboards for producer throughput and error rates.
- Add Snowpipe or external tables for loading Databricks Gold outputs into Snowflake.
- Add DataHub or OpenMetadata lineage ingestion from dbt artifacts.
- Add contract tests with JSON Schema or AWS Glue Schema Registry.

