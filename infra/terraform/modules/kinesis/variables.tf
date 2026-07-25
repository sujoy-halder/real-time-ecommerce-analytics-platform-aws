variable "project_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "shard_count" {
  type    = number
  default = 2
}

variable "retention_hours" {
  type    = number
  default = 48
}

variable "tags" {
  type    = map(string)
  default = {}
}

