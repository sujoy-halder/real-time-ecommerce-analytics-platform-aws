<div align="center">

# Real-Time E-Commerce Analytics Platform on AWS

### Portfolio-grade streaming analytics platform for high-volume e-commerce events using AWS, Kinesis, Databricks, Snowflake, dbt, Airflow, Terraform, Kubernetes, Docker, and CI/CD.

![AWS](https://img.shields.io/badge/AWS-Cloud%20Platform-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![Python](https://img.shields.io/badge/Python-Microservices-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Kinesis](https://img.shields.io/badge/Amazon%20Kinesis-Streaming-FF4F8B?style=for-the-badge&logo=amazonaws&logoColor=white)
![Databricks](https://img.shields.io/badge/Databricks-Lakehouse-FF3621?style=for-the-badge&logo=databricks&logoColor=white)
![Snowflake](https://img.shields.io/badge/Snowflake-Warehouse-29B5E8?style=for-the-badge&logo=snowflake&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-Analytics%20Engineering-FF694B?style=for-the-badge&logo=dbt&logoColor=white)
![Airflow](https://img.shields.io/badge/Airflow-Orchestration-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-IaC-844FBA?style=for-the-badge&logo=terraform&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-EKS-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containers-2496ED?style=for-the-badge&logo=docker&logoColor=white)

</div>

---

## Project Overview

**Real-Time E-Commerce Analytics Platform on AWS** is a production-style data engineering project that processes high-volume e-commerce events such as orders, clicks, payments, customer sessions, product views, and shipment updates.

The platform moves events from containerized Python producers into AWS streaming infrastructure, stores immutable raw data in an S3 Bronze layer, refines it with Databricks Structured Streaming and Delta Lake, and publishes analytics-ready Snowflake marts using dbt.

---

## What This Demonstrates

| Area | Implementation |
|---|---|
| Real-Time Ingestion | Python producers, Amazon Kinesis, Lambda |
| Data Lake | S3 Bronze raw JSON storage |
| Lakehouse Processing | Databricks Structured Streaming, Delta Lake |
| Warehouse Modeling | Snowflake, dbt star schemas, tests, docs |
| Data Quality | dbt tests, Great Expectations |
| Orchestration | Airflow |
| Infrastructure | Terraform |
| Deployment | Docker, Kubernetes, Helm, GitHub Actions |
| Monitoring | CloudWatch, Prometheus, Grafana |
| Governance | Informatica IICS, OpenMetadata touchpoints |

---

## Architecture

```mermaid
flowchart LR
    Producers["Python Producers on EKS"] --> Kinesis["Amazon Kinesis Streams"]
    Kinesis --> Lambda["Lambda Raw Event Consumer"]
    Lambda --> Bronze["S3 Bronze Raw JSON"]
    Bronze --> Databricks["Databricks Structured Streaming"]
    Databricks --> Silver["Delta Silver Tables"]
    Silver --> Gold["Delta Gold Tables"]
    Gold --> Snowflake["Snowflake Curated Warehouse"]
    Snowflake --> DBT["dbt Star Schema + Tests + Docs"]
    DBT --> BI["BI / Analytics / ML Features"]

    Informatica["Informatica IICS CDC + Enterprise Sources"] --> Bronze
    CloudWatch["CloudWatch + Prometheus + Grafana"] -. monitors .-> Producers
    CloudWatch -. monitors .-> Kinesis
    CloudWatch -. monitors .-> Lambda

    classDef source fill:#DBEAFE,stroke:#2563EB,color:#111827;
    classDef stream fill:#FCE7F3,stroke:#DB2777,color:#111827;
    classDef aws fill:#FEF3C7,stroke:#F59E0B,color:#111827;
    classDef lake fill:#CCFBF1,stroke:#0D9488,color:#111827;
    classDef warehouse fill:#EDE9FE,stroke:#7C3AED,color:#111827;
    classDef monitor fill:#DCFCE7,stroke:#16A34A,color:#111827;

    class Producers,Informatica source;
    class Kinesis,Lambda stream;
    class Bronze aws;
    class Databricks,Silver,Gold lake;
    class Snowflake,DBT,BI warehouse;
    class CloudWatch monitor;
```

---

## Data Flow

```mermaid
flowchart TD
    Events["E-Commerce Events"] --> Stream["Kinesis Streaming Layer"]
    Stream --> Bronze["S3 Bronze"]
    Bronze --> Silver["Databricks Silver"]
    Silver --> Gold["Databricks Gold"]
    Gold --> Warehouse["Snowflake Warehouse"]
    Warehouse --> Marts["dbt Analytics Marts"]

    classDef events fill:#DBEAFE,stroke:#2563EB,color:#111827;
    classDef streaming fill:#FCE7F3,stroke:#DB2777,color:#111827;
    classDef bronze fill:#FEF3C7,stroke:#F59E0B,color:#111827;
    classDef silver fill:#E5E7EB,stroke:#6B7280,color:#111827;
    classDef gold fill:#FDE68A,stroke:#D97706,color:#111827;
    classDef marts fill:#EDE9FE,stroke:#7C3AED,color:#111827;

    class Events events;
    class Stream streaming;
    class Bronze bronze;
    class Silver silver;
    class Gold gold;
    class Warehouse,Marts marts;
```

---

## Repository Map

```text
services/               Python producers, FastAPI API, Lambda consumer
infra/terraform/        AWS, Snowflake, and monitoring infrastructure
k8s/helm/               Helm chart for producer and API workloads on EKS
databricks/             Streaming ETL notebook and job specification
dbt/                    Snowflake models, tests, docs, and marts
airflow/                Orchestration DAG for lakehouse-to-warehouse flow
great_expectations/     Data quality suite
openmetadata/           Metadata ingestion configuration
docs/                   Architecture notes, interview guide, and runbook
.github/workflows/      CI/CD pipeline
```

---

## Local Quickstart

```bash
docker compose up --build
```

Create the local Bronze S3 bucket for Lambda testing:

```bash
python scripts/bootstrap_localstack.py
```

Run tests:

```bash
python scripts/run_tests.py
```

---

## Event Types

| Event | Purpose |
|---|---|
| `order_created` | Captures new customer orders |
| `cart_updated` | Tracks cart behavior |
| `product_viewed` | Captures clickstream activity |
| `payment_authorized` | Tracks payment events |
| `customer_session_started` | Starts customer session analysis |
| `shipment_status_changed` | Tracks fulfillment and logistics |

---

## Author

**Sujoy Halder**  
AWS | Python | Databricks | Snowflake | dbt | Airflow | Terraform | Kubernetes

<div align="center">

### Built for real-time cloud data engineering portfolios

![Real Time](https://img.shields.io/badge/Analytics-Real%20Time-DB2777?style=for-the-badge)
![Lakehouse](https://img.shields.io/badge/Architecture-Lakehouse-00A6A6?style=for-the-badge)
![Ecommerce](https://img.shields.io/badge/Domain-E--Commerce-2563EB?style=for-the-badge)
![Portfolio](https://img.shields.io/badge/Type-Portfolio%20Project-16A34A?style=for-the-badge)

</div>
