variable "project_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "bucket_force_destroy" {
  type    = bool
  default = false
}

variable "tags" {
  type    = map(string)
  default = {}
}

