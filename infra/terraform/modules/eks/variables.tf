variable "project_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "private_subnet_ids" {
  type = list(string)
}

variable "kinesis_stream_arn" {
  type        = string
  description = "Kinesis stream ARN that producer pods can write to."
}

variable "tags" {
  type    = map(string)
  default = {}
}
