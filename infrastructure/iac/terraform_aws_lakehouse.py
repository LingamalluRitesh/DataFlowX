"""
DataFlowX AWS Terraform HCL Infrastructure Generator
Generates production-ready Terraform HCL code for AWS S3 lakehouse storage, AWS Glue catalog, AWS KMS encryption keys, and EKS worker clusters.
"""

class TerraformAWSGenerator:
    """Generates AWS Terraform modules."""

    @classmethod
    def generate_lakehouse_hcl(cls, environment: str = "production", bucket_name: str = "dataflowx-lakehouse-prod") -> str:
        hcl = f"""
# Terraform Configuration for AWS Lakehouse ({environment})
terraform {{
  required_version = ">= 1.5.0"
  required_providers {{
    aws = {{
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }}
  }}
}}

resource "aws_kms_key" "lakehouse_key" {{
  description             = "KMS CMK for DataFlowX Lakehouse"
  deletion_window_in_days = 30
  enable_key_rotation     = true
}}

resource "aws_s3_bucket" "lakehouse_bucket" {{
  bucket = "{bucket_name}"
}}

resource "aws_s3_bucket_server_side_encryption_configuration" "lakehouse_enc" {{
  bucket = aws_s3_bucket.lakehouse_bucket.id
  rule {{
    apply_server_side_encryption_by_default {{
      kms_master_key_id = aws_kms_key.lakehouse_key.arn
      sse_algorithm     = "aws:kms"
    }}
  }}
}}

resource "aws_glue_catalog_database" "lakehouse_db" {{
  name = "dataflowx_{environment}"
}}
        """.strip()
        return hcl
