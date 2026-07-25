resource "aws_cloudwatch_metric_alarm" "kinesis_write_throttles" {
  alarm_name          = "${var.project_name}-${var.environment}-kinesis-write-throttles"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "WriteProvisionedThroughputExceeded"
  namespace           = "AWS/Kinesis"
  period              = 60
  statistic           = "Sum"
  threshold           = 0
  alarm_description   = "Kinesis stream is throttling producer writes."

  dimensions = {
    StreamName = var.kinesis_stream_name
  }

  tags = var.tags
}

resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  alarm_name          = "${var.project_name}-${var.environment}-lambda-errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 60
  statistic           = "Sum"
  threshold           = 0
  alarm_description   = "Lambda consumer is returning errors."

  dimensions = {
    FunctionName = var.lambda_function_name
  }

  tags = var.tags
}

