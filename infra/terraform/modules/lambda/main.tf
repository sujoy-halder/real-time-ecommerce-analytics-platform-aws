locals {
  function_name = "${var.project_name}-${var.environment}-kinesis-to-s3"
  package_path  = "${path.root}/${local.function_name}.zip"
}

data "archive_file" "lambda_package" {
  type        = "zip"
  source_file = var.source_file
  output_path = local.package_path
}

resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${local.function_name}"
  retention_in_days = 30
  tags              = var.tags
}

resource "aws_lambda_function" "kinesis_to_s3" {
  function_name = local.function_name
  description   = "Writes e-commerce Kinesis events to the S3 Bronze layer."
  role          = var.lambda_role_arn
  handler       = "handler.handler"
  runtime       = "python3.12"
  memory_size   = var.memory_size
  timeout       = var.timeout

  filename         = data.archive_file.lambda_package.output_path
  source_code_hash = data.archive_file.lambda_package.output_base64sha256

  environment {
    variables = {
      BRONZE_BUCKET = var.bronze_bucket_name
      AWS_REGION    = data.aws_region.current.name
    }
  }

  depends_on = [aws_cloudwatch_log_group.lambda]
  tags       = var.tags
}

resource "aws_lambda_event_source_mapping" "kinesis" {
  event_source_arn                   = var.kinesis_stream_arn
  function_name                      = aws_lambda_function.kinesis_to_s3.arn
  starting_position                  = "LATEST"
  batch_size                         = var.batch_size
  maximum_batching_window_in_seconds = 5
  function_response_types            = ["ReportBatchItemFailures"]
}

data "aws_region" "current" {}

