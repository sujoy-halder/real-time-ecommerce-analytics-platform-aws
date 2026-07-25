variable "project_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "kinesis_stream_name" {
  type = string
}

variable "lambda_function_name" {
  type = string
}

variable "tags" {
  type    = map(string)
  default = {}
}

