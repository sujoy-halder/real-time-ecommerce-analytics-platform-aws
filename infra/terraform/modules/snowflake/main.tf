locals {
  database_name  = upper(replace("${var.project_name}_${var.environment}", "-", "_"))
  warehouse_name = upper(replace("${var.project_name}_${var.environment}_wh", "-", "_"))
}

resource "snowflake_database" "analytics" {
  name    = local.database_name
  comment = "Curated e-commerce analytics database managed by Terraform."
}

resource "snowflake_schema" "analytics" {
  database = snowflake_database.analytics.name
  name     = "ANALYTICS"
  comment  = "dbt-owned analytics schema."
}

resource "snowflake_schema" "raw" {
  database = snowflake_database.analytics.name
  name     = "RAW"
  comment  = "Landing schema for external tables and Snowpipe loads."
}

resource "snowflake_table" "gold_customer_orders_daily" {
  database = snowflake_database.analytics.name
  schema   = snowflake_schema.raw.name
  name     = "GOLD_CUSTOMER_ORDERS_DAILY"
  comment  = "Databricks Gold daily customer order aggregates."

  column {
    name = "EVENT_DATE"
    type = "DATE"
  }
  column {
    name = "CUSTOMER_ID"
    type = "VARCHAR"
  }
  column {
    name = "ORDERS"
    type = "NUMBER"
  }
  column {
    name = "GROSS_REVENUE"
    type = "NUMBER(18,2)"
  }
  column {
    name = "LAST_ORDER_AT"
    type = "TIMESTAMP_NTZ"
  }
  column {
    name = "_UPDATED_AT"
    type = "TIMESTAMP_NTZ"
  }
}

resource "snowflake_table" "gold_customer_payments_daily" {
  database = snowflake_database.analytics.name
  schema   = snowflake_schema.raw.name
  name     = "GOLD_CUSTOMER_PAYMENTS_DAILY"
  comment  = "Databricks Gold daily customer payment aggregates."

  column {
    name = "EVENT_DATE"
    type = "DATE"
  }
  column {
    name = "CUSTOMER_ID"
    type = "VARCHAR"
  }
  column {
    name = "PAYMENT_EVENTS"
    type = "NUMBER"
  }
  column {
    name = "AUTHORIZED_PAYMENT_AMOUNT"
    type = "NUMBER(18,2)"
  }
  column {
    name = "_UPDATED_AT"
    type = "TIMESTAMP_NTZ"
  }
}

resource "snowflake_table" "silver_events" {
  database = snowflake_database.analytics.name
  schema   = snowflake_schema.raw.name
  name     = "SILVER_EVENTS"
  comment  = "Deduplicated event stream exported from Databricks Silver."

  column {
    name = "EVENT_ID"
    type = "VARCHAR"
  }
  column {
    name = "EVENT_TYPE"
    type = "VARCHAR"
  }
  column {
    name = "EVENT_TIME"
    type = "TIMESTAMP_NTZ"
  }
  column {
    name = "EVENT_DATE"
    type = "DATE"
  }
  column {
    name = "CUSTOMER_ID"
    type = "VARCHAR"
  }
  column {
    name = "ORDER_ID"
    type = "VARCHAR"
  }
  column {
    name = "PRODUCT_ID"
    type = "VARCHAR"
  }
  column {
    name = "SESSION_ID"
    type = "VARCHAR"
  }
  column {
    name = "ORDER_AMOUNT"
    type = "NUMBER(18,2)"
  }
  column {
    name = "PAYMENT_AMOUNT"
    type = "NUMBER(18,2)"
  }
  column {
    name = "PAYLOAD"
    type = "VARCHAR"
  }
  column {
    name = "_INGESTED_AT"
    type = "TIMESTAMP_NTZ"
  }
}

resource "snowflake_warehouse" "transforming" {
  name                = local.warehouse_name
  warehouse_size      = "XSMALL"
  auto_suspend        = 60
  auto_resume         = true
  initially_suspended = true
}
