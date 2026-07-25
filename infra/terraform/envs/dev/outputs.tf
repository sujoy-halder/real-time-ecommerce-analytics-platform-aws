output "bronze_bucket_name" {
  value = module.s3.bronze_bucket_name
}

output "kinesis_stream_name" {
  value = module.kinesis.stream_name
}

output "eks_cluster_name" {
  value = module.eks.cluster_name
}

output "snowflake_database" {
  value = module.snowflake.database_name
}

