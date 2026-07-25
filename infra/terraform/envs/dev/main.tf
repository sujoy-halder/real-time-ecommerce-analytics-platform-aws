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

module "ecr" {
  source       = "../../modules/ecr"
  project_name = var.project_name
  environment  = var.environment
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

module "lambda" {
  source             = "../../modules/lambda"
  project_name       = var.project_name
  environment        = var.environment
  lambda_role_arn    = module.iam.lambda_role_arn
  kinesis_stream_arn = module.kinesis.stream_arn
  bronze_bucket_name = module.s3.bronze_bucket_name
  source_file        = abspath("${path.root}/../../../../services/lambda-consumer/handler.py")
  tags               = local.tags

  depends_on = [module.iam]
}

module "eks" {
  source             = "../../modules/eks"
  project_name       = var.project_name
  environment        = var.environment
  vpc_id             = var.vpc_id
  private_subnet_ids = var.private_subnet_ids
  kinesis_stream_arn = module.kinesis.stream_arn
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
  lambda_function_name = module.lambda.function_name
  tags                 = local.tags
}
