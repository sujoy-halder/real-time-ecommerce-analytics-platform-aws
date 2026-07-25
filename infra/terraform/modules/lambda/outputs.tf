output "function_name" {
  value = aws_lambda_function.kinesis_to_s3.function_name
}

output "function_arn" {
  value = aws_lambda_function.kinesis_to_s3.arn
}

output "event_source_mapping_uuid" {
  value = aws_lambda_event_source_mapping.kinesis.uuid
}

