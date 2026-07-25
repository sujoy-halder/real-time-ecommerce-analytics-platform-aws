data "aws_iam_policy_document" "producer_kinesis_access" {
  statement {
    actions = [
      "kinesis:DescribeStream",
      "kinesis:DescribeStreamSummary",
      "kinesis:ListShards",
      "kinesis:PutRecord",
      "kinesis:PutRecords"
    ]
    resources = [var.kinesis_stream_arn]
  }
}

resource "aws_iam_policy" "producer_kinesis_access" {
  name   = "${var.project_name}-${var.environment}-producer-kinesis-access"
  policy = data.aws_iam_policy_document.producer_kinesis_access.json
  tags   = var.tags
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = "${var.project_name}-${var.environment}"
  cluster_version = "1.30"

  vpc_id     = var.vpc_id
  subnet_ids = var.private_subnet_ids

  enable_cluster_creator_admin_permissions = true

  eks_managed_node_groups = {
    default = {
      min_size       = 2
      max_size       = 8
      desired_size   = 3
      instance_types = ["m6i.large"]
      capacity_type  = "ON_DEMAND"
      iam_role_additional_policies = {
        ProducerKinesisAccess = aws_iam_policy.producer_kinesis_access.arn
      }
    }
  }

  tags = var.tags
}
