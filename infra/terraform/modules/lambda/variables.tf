variable "project_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "lambda_role_arn" {
  type = string
}

variable "kinesis_stream_arn" {
  type = string
}

variable "bronze_bucket_name" {
  type = string
}

variable "source_file" {
  type        = string
  description = "Path to the Lambda handler.py file."
}

variable "memory_size" {
  type    = number
  default = 256
}

variable "timeout" {
  type    = number
  default = 60
}

variable "batch_size" {
  type    = number
  default = 100
}

variable "tags" {
  type    = map(string)
  default = {}
}

