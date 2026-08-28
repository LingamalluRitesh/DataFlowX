"""
DataFlowX GCP Terraform HCL Infrastructure Generator
Generates Google Cloud Terraform HCL for GCS multi-region storage buckets, BigQuery datasets, and Cloud KMS key rings.
"""

class TerraformGCPGenerator:
    """Generates GCP Terraform modules."""

    @classmethod
    def generate_lakehouse_hcl(cls, project_id: str = "dataflowx-prod", location: str = "US") -> str:
        hcl = f"""
# Terraform Configuration for Google Cloud Lakehouse ({project_id})
resource "google_storage_bucket" "lakehouse_gcs" {{
  name          = "{project_id}-lakehouse"
  location      = "{location}"
  force_destroy = false
  uniform_bucket_level_access = true
}}

resource "google_bigquery_dataset" "lakehouse_bq" {{
  dataset_id                  = "dataflowx_gold"
  friendly_name               = "DataFlowX Gold Analytics"
  location                    = "{location}"
}}
        """.strip()
        return hcl
