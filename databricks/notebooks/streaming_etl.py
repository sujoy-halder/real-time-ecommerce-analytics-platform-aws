# Databricks notebook source
# Real-time e-commerce streaming ETL.
# Reads raw JSON from S3 Bronze, validates and deduplicates events, and writes Delta tables.

from pyspark.sql import functions as F
from pyspark.sql.types import (
    MapType,
    StringType,
    StructField,
    StructType,
    TimestampType,
)


dbutils.widgets.text("bronze_path", "s3://ecommerce-analytics-dev-bronze/events")
dbutils.widgets.text("checkpoint_path", "s3://ecommerce-analytics-dev-bronze/checkpoints/ecommerce")
dbutils.widgets.text("catalog", "ecommerce_analytics")
dbutils.widgets.text("schema", "lakehouse")

bronze_path = dbutils.widgets.get("bronze_path")
checkpoint_path = dbutils.widgets.get("checkpoint_path")
catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")

spark.sql(f"CREATE CATALOG IF NOT EXISTS {catalog}")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema}")
spark.sql(f"USE CATALOG {catalog}")
spark.sql(f"USE SCHEMA {schema}")


event_schema = StructType(
    [
        StructField("event_id", StringType(), False),
        StructField("event_type", StringType(), False),
        StructField("event_time", TimestampType(), False),
        StructField("customer_id", StringType(), False),
        StructField("source", StringType(), False),
        StructField("schema_version", StringType(), False),
        StructField("payload", MapType(StringType(), StringType()), True),
    ]
)


raw_events = (
    spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "json")
    .option("cloudFiles.schemaLocation", f"{checkpoint_path}/schema/raw")
    .option("primitivesAsString", "true")
    .schema(event_schema)
    .load(bronze_path)
    .withColumn("_ingested_at", F.current_timestamp())
    .withColumn("_source_file", F.input_file_name())
)


is_valid_event = (
    F.col("event_id").isNotNull()
    & F.col("event_type").isNotNull()
    & F.col("event_time").isNotNull()
    & F.col("customer_id").isNotNull()
)

valid_events = raw_events.where(is_valid_event)
invalid_events = raw_events.where(~is_valid_event)

(
    invalid_events.writeStream.format("delta")
    .option("checkpointLocation", f"{checkpoint_path}/bad_records")
    .outputMode("append")
    .toTable(f"{catalog}.{schema}.bad_events")
)


bronze_query = (
    valid_events.writeStream.format("delta")
    .option("checkpointLocation", f"{checkpoint_path}/bronze")
    .outputMode("append")
    .toTable(f"{catalog}.{schema}.bronze_events")
)


silver_events = (
    valid_events.withWatermark("event_time", "15 minutes")
    .dropDuplicates(["event_id"])
    .withColumn("event_date", F.to_date("event_time"))
    .withColumn("order_id", F.col("payload").getItem("order_id"))
    .withColumn("product_id", F.col("payload").getItem("product_id"))
    .withColumn("session_id", F.col("payload").getItem("session_id"))
    .withColumn("order_amount", F.col("payload").getItem("order_amount").cast("decimal(18,2)"))
    .withColumn("payment_amount", F.col("payload").getItem("payment_amount").cast("decimal(18,2)"))
)

silver_query = (
    silver_events.writeStream.format("delta")
    .option("checkpointLocation", f"{checkpoint_path}/silver")
    .outputMode("append")
    .partitionBy("event_date", "event_type")
    .toTable(f"{catalog}.{schema}.silver_events")
)


orders = silver_events.where(F.col("event_type") == "order_created")
payments = silver_events.where(F.col("event_type") == "payment_authorized")
sessions = silver_events.where(F.col("session_id").isNotNull())

gold_orders = (
    orders.groupBy("event_date", "customer_id")
    .agg(
        F.countDistinct("order_id").alias("orders"),
        F.sum("order_amount").alias("gross_revenue"),
        F.max("event_time").alias("last_order_at"),
    )
    .withColumn("_updated_at", F.current_timestamp())
)

gold_payments = (
    payments.groupBy("event_date", "customer_id")
    .agg(
        F.count("*").alias("payment_events"),
        F.sum("payment_amount").alias("authorized_payment_amount"),
    )
    .withColumn("_updated_at", F.current_timestamp())
)

gold_sessions = (
    sessions.withWatermark("event_time", "30 minutes")
    .groupBy(
        F.window("event_time", "30 minutes"),
        "customer_id",
        "session_id",
    )
    .agg(
        F.min("event_time").alias("session_started_at"),
        F.max("event_time").alias("session_last_seen_at"),
        F.count("*").alias("events_in_session"),
    )
    .withColumn("_updated_at", F.current_timestamp())
)

(
    gold_orders.writeStream.format("delta")
    .option("checkpointLocation", f"{checkpoint_path}/gold_orders")
    .outputMode("complete")
    .toTable(f"{catalog}.{schema}.gold_customer_orders_daily")
)

(
    gold_payments.writeStream.format("delta")
    .option("checkpointLocation", f"{checkpoint_path}/gold_payments")
    .outputMode("complete")
    .toTable(f"{catalog}.{schema}.gold_customer_payments_daily")
)

(
    gold_sessions.writeStream.format("delta")
    .option("checkpointLocation", f"{checkpoint_path}/gold_sessions")
    .outputMode("append")
    .toTable(f"{catalog}.{schema}.gold_customer_sessions")
)

spark.streams.awaitAnyTermination()
