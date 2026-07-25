from __future__ import annotations

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator


default_args = {
    "owner": "data-platform",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id="ecommerce_analytics_orchestration",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule="0 * * * *",
    catchup=False,
    max_active_runs=1,
    tags=["ecommerce", "streaming", "lakehouse"],
) as dag:
    start = EmptyOperator(task_id="start")

    informatica_cdc_ingestion = BashOperator(
        task_id="informatica_cdc_ingestion",
        bash_command=(
            "echo 'Trigger Informatica IICS CDC taskflow for SAP/CRM ingestion via REST API'"
        ),
    )

    run_databricks_streaming_job = BashOperator(
        task_id="run_databricks_streaming_job",
        bash_command=(
            "databricks jobs run-now "
            "--job-id ${DATABRICKS_ECOMMERCE_STREAMING_JOB_ID}"
        ),
    )

    snowflake_load_gold = BashOperator(
        task_id="snowflake_load_gold",
        bash_command=(
            "snowsql -q \"call raw.load_databricks_gold_tables();\""
        ),
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        cwd="/opt/airflow/dbt",
        bash_command="dbt deps && dbt run --select marts",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        cwd="/opt/airflow/dbt",
        bash_command="dbt test --select marts",
    )

    publish_metadata = BashOperator(
        task_id="publish_metadata",
        bash_command=(
            "echo 'Run OpenMetadata ingestion and publish dbt docs artifacts'"
        ),
    )

    end = EmptyOperator(task_id="end")

    (
        start
        >> informatica_cdc_ingestion
        >> run_databricks_streaming_job
        >> snowflake_load_gold
        >> dbt_run
        >> dbt_test
        >> publish_metadata
        >> end
    )

