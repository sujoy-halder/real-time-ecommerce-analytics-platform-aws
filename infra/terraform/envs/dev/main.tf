locals {
  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

module "s3" {
  source       = "../../modules/s3"
  project_name = var.project_name
  environment  = var.environment
  tags         = local.tags
}

module "kinesis" {
  source       = "../../modules/kinesis"
  project_name = var.project_name
  environment  = var.environment
  shard_count  = 4
  tags         = local.tags
}

module "iam" {
  source             = "../../modules/iam"
  project_name       = var.project_name
  environment        = var.environment
  bronze_bucket_arn  = module.s3.bronze_bucket_arn
  kinesis_stream_arn = module.kinesis.stream_arn
  tags               = local.tags
}

module "eks" {
  source             = "../../modules/eks"
  project_name       = var.project_name
  environment        = var.environment
  vpc_id             = var.vpc_id
  private_subnet_ids = var.private_subnet_ids
  tags               = local.tags
}

module "snowflake" {
  source       = "../../modules/snowflake"
  project_name = var.project_name
  environment  = var.environment
}

module "monitoring" {
  source               = "../../modules/monitoring"
  project_name         = var.project_name
  environment          = var.environment
  kinesis_stream_name  = module.kinesis.stream_name
  lambda_function_name = "${var.project_name}-${var.environment}-kinesis-to-s3"
  tags                 = local.tags
}

