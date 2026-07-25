output "bronze_bucket_name" {
  value = module.s3.bronze_bucket_name
}

output "kinesis_stream_name" {
  value = module.kinesis.stream_name
}

output "eks_cluster_name" {
  value = module.eks.cluster_name
}

output "lambda_function_name" {
  value = module.lambda.function_name
}

output "producer_ecr_repository_url" {
  value = module.ecr.producer_repository_url
}

output "api_ecr_repository_url" {
  value = module.ecr.api_repository_url
}

output "snowflake_database" {
  value = module.snowflake.database_name
}

output "snowflake_warehouse" {
  value = module.snowflake.warehouse_name
}
