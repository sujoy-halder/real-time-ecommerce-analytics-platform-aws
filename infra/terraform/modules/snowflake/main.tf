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

resource "snowflake_warehouse" "transforming" {
  name                = local.warehouse_name
  warehouse_size      = "XSMALL"
  auto_suspend        = 60
  auto_resume         = true
  initially_suspended = true
}

