variable "project_name" {
  type        = string
  description = "Project name used for resource names."
  default     = "ecommerce-analytics"
}

variable "environment" {
  type        = string
  description = "Deployment environment."
  default     = "dev"
}

variable "aws_region" {
  type        = string
  description = "AWS region."
  default     = "us-east-1"
}

variable "vpc_id" {
  type        = string
  description = "Existing VPC ID for EKS."
}

variable "private_subnet_ids" {
  type        = list(string)
  description = "Private subnet IDs for EKS node groups."
}

variable "snowflake_account" {
  type        = string
  description = "Snowflake account identifier."
  sensitive   = true
}

variable "snowflake_user" {
  type        = string
  description = "Snowflake user."
  sensitive   = true
}

variable "snowflake_password" {
  type        = string
  description = "Snowflake password."
  sensitive   = true
}

variable "snowflake_role" {
  type        = string
  description = "Snowflake role used by Terraform."
  default     = "SYSADMIN"
}

