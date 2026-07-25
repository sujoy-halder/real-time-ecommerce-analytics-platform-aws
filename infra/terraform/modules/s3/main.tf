locals {
  bucket_prefix = lower(replace("${var.project_name}-${var.environment}", "_", "-"))
}

resource "aws_s3_bucket" "bronze" {
  bucket        = "${local.bucket_prefix}-bronze"
  force_destroy = var.bucket_force_destroy
  tags          = var.tags
}

resource "aws_s3_bucket" "silver" {
  bucket        = "${local.bucket_prefix}-silver"
  force_destroy = var.bucket_force_destroy
  tags          = var.tags
}

resource "aws_s3_bucket" "gold" {
  bucket        = "${local.bucket_prefix}-gold"
  force_destroy = var.bucket_force_destroy
  tags          = var.tags
}

resource "aws_s3_bucket_public_access_block" "all" {
  for_each = {
    bronze = aws_s3_bucket.bronze.id
    silver = aws_s3_bucket.silver.id
    gold   = aws_s3_bucket.gold.id
  }

  bucket                  = each.value
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "all" {
  for_each = {
    bronze = aws_s3_bucket.bronze.id
    silver = aws_s3_bucket.silver.id
    gold   = aws_s3_bucket.gold.id
  }

  bucket = each.value

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "all" {
  for_each = {
    bronze = aws_s3_bucket.bronze.id
    silver = aws_s3_bucket.silver.id
    gold   = aws_s3_bucket.gold.id
  }

  bucket = each.value

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "bronze" {
  bucket = aws_s3_bucket.bronze.id

  rule {
    id     = "raw-event-retention"
    status = "Enabled"

    filter {
      prefix = "events/"
    }

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 180
      storage_class = "GLACIER"
    }
  }
}

