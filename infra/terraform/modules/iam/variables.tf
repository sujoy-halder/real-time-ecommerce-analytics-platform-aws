variable "project_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "bronze_bucket_arn" {
  type = string
}

variable "kinesis_stream_arn" {
  type = string
}

variable "tags" {
  type    = map(string)
  default = {}
}

