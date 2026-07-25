resource "aws_kinesis_stream" "events" {
  name             = "${var.project_name}-${var.environment}-events"
  shard_count      = var.shard_count
  retention_period = var.retention_hours

  stream_mode_details {
    stream_mode = "PROVISIONED"
  }

  tags = var.tags
}

