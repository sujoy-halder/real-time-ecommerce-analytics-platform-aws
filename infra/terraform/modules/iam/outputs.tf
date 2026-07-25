output "lambda_role_arn" {
  value = aws_iam_role.lambda_kinesis_to_s3.arn
}

