# Deployment Guide

## Prerequisites

- AWS account with an existing VPC and at least two private subnets.
- GitHub Actions OIDC role with permission to manage ECR, EKS, S3, Kinesis, Lambda, IAM, CloudWatch, and DynamoDB state locking.
- Snowflake account and user/role that can create the analytics database, schemas, and warehouse.
- Optional Databricks workspace token for bundle deployment.
- Docker, Terraform, Helm, and dbt if deploying manually from a workstation.

## GitHub Actions Deployment

Set these repository or environment secrets:

```text
AWS_ROLE_TO_ASSUME
TF_STATE_BUCKET
TF_LOCK_TABLE
AWS_VPC_ID
AWS_PRIVATE_SUBNET_IDS_JSON
SNOWFLAKE_ACCOUNT
SNOWFLAKE_USER
SNOWFLAKE_PASSWORD
SNOWFLAKE_ROLE
DATABRICKS_HOST
DATABRICKS_TOKEN
SNOWFLAKE_URL
DATABRICKS_SNOWFLAKE_SECRET_SCOPE
```

`AWS_PRIVATE_SUBNET_IDS_JSON` must be a JSON list:

```json
["subnet-0123456789abcdef0", "subnet-0fedcba9876543210"]
```

On push to `main`, the workflow:

1. Runs Python tests, Terraform validation, Helm lint, and dbt parse.
2. Builds Docker images as a validation gate.
3. Applies Terraform using S3 remote state and DynamoDB state locking.
4. Creates ECR repositories, S3, Kinesis, IAM, Lambda, EKS, Snowflake, and CloudWatch.
5. Builds and pushes producer/API images to ECR.
6. Deploys producer/API workloads to EKS with Helm.
7. Deploys the Databricks bundle when Databricks and Snowflake URL secrets exist.
8. Runs dbt models and tests against Snowflake.

The Terraform state backend bucket and lock table must exist before the first deployment. A minimal bootstrap looks like:

```bash
aws s3api create-bucket --bucket <your-tf-state-bucket> --region us-east-1
aws dynamodb create-table \
  --table-name <your-tf-lock-table> \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST
```

## Manual Deployment

```bash
cd infra/terraform/envs/dev
cp terraform.tfvars.example terraform.tfvars
terraform init \
  -backend-config="bucket=<your-tf-state-bucket>" \
  -backend-config="key=ecommerce-analytics/dev/terraform.tfstate" \
  -backend-config="region=us-east-1" \
  -backend-config="dynamodb_table=<your-tf-lock-table>" \
  -backend-config="encrypt=true"
terraform plan
terraform apply
```

Then deploy Kubernetes workloads:

```bash
aws eks update-kubeconfig --name "$(terraform output -raw eks_cluster_name)" --region us-east-1
helm upgrade --install ecommerce ../../../../k8s/helm/ecommerce-streaming \
  --namespace ecommerce --create-namespace \
  --set global.kinesisStreamName="$(terraform output -raw kinesis_stream_name)" \
  --set producer.image.repository="$(terraform output -raw producer_ecr_repository_url)" \
  --set api.image.repository="$(terraform output -raw api_ecr_repository_url)"
```
