# Runbook

## Local Development

Start the local stack:

```bash
docker compose up --build
```

The Docker producer and local consumer create the local Kinesis stream and Bronze S3 bucket automatically. To bootstrap them manually:

```bash
python scripts/bootstrap_localstack.py
```

Check that local events reached the Bronze bucket:

```bash
python scripts/check_local_bronze.py
```

Run Python service tests:

```bash
python scripts/run_tests.py
```

## Terraform

From the dev environment:

```bash
cd infra/terraform/envs/dev
terraform init
terraform fmt -recursive
terraform validate
terraform plan
```

Required variables include AWS region, environment name, Snowflake account information, and Kubernetes settings.

For GitHub Actions deployment, set `AWS_PRIVATE_SUBNET_IDS_JSON` as a Terraform-compatible JSON list, for example:

```json
["subnet-aaa111", "subnet-bbb222"]
```

## dbt

```bash
cd dbt
dbt deps
dbt seed
dbt run
dbt test
dbt docs generate
```

## Operational Checks

- Kinesis incoming records should be greater than zero.
- Lambda iterator age should stay low under normal load.
- Bronze S3 partitions should appear by event type and ingestion hour.
- Databricks checkpoints should advance continuously.
- dbt source freshness should pass before downstream marts run.

## Incident Response

1. Check Kinesis throttling, iterator age, and producer logs.
2. Inspect Lambda failures and dead-letter destinations.
3. Validate whether malformed records are isolated in the bad-record path.
4. Replay from Bronze if Silver or Gold transformations need correction.
5. Re-run dbt models with incremental predicates disabled only after confirming the replay window.
