# Databricks notebook source
# Loads Databricks Silver/Gold Delta tables into Snowflake RAW tables for dbt.

from pyspark.sql import functions as F

dbutils.widgets.text("catalog", "ecommerce_analytics")
dbutils.widgets.text("schema", "lakehouse")
dbutils.widgets.text("sf_url", "")
dbutils.widgets.text("sf_database", "ECOMMERCE_ANALYTICS_DEV")
dbutils.widgets.text("sf_schema", "RAW")
dbutils.widgets.text("sf_warehouse", "ECOMMERCE_ANALYTICS_DEV_WH")
dbutils.widgets.text("sf_secret_scope", "ecommerce")
dbutils.widgets.text("sf_user_secret_key", "snowflake-user")
dbutils.widgets.text("sf_password_secret_key", "snowflake-password")

catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")
sf_url = dbutils.widgets.get("sf_url")
sf_database = dbutils.widgets.get("sf_database")
sf_schema = dbutils.widgets.get("sf_schema")
sf_warehouse = dbutils.widgets.get("sf_warehouse")
sf_secret_scope = dbutils.widgets.get("sf_secret_scope")
sf_user_secret_key = dbutils.widgets.get("sf_user_secret_key")
sf_password_secret_key = dbutils.widgets.get("sf_password_secret_key")

sf_options = {
    "sfURL": sf_url,
    "sfUser": dbutils.secrets.get(sf_secret_scope, sf_user_secret_key),
    "sfPassword": dbutils.secrets.get(sf_secret_scope, sf_password_secret_key),
    "sfDatabase": sf_database,
    "sfSchema": sf_schema,
    "sfWarehouse": sf_warehouse,
}

table_map = {
    f"{catalog}.{schema}.gold_customer_orders_daily": "GOLD_CUSTOMER_ORDERS_DAILY",
    f"{catalog}.{schema}.gold_customer_payments_daily": "GOLD_CUSTOMER_PAYMENTS_DAILY",
    f"{catalog}.{schema}.silver_events": "SILVER_EVENTS",
}

for source_table, target_table in table_map.items():
    dataframe = spark.table(source_table)

    if target_table == "SILVER_EVENTS":
        dataframe = dataframe.withColumn("payload", F.to_json(F.col("payload")))

    (
        dataframe
        .write.format("snowflake")
        .options(**sf_options)
        .option("dbtable", target_table)
        .mode("overwrite")
        .save()
    )
