"""
DataFlowX Azure Terraform HCL Infrastructure Generator
Generates Azure Terraform HCL for ADLS Gen2 storage accounts, Synapse workspaces, and Azure Key Vault HSM keys.
"""

class TerraformAzureGenerator:
    """Generates Azure Terraform modules."""

    @classmethod
    def generate_lakehouse_hcl(cls, resource_group: str = "rg-dataflowx-prod", location: str = "eastus2") -> str:
        hcl = f"""
# Terraform Configuration for Azure Lakehouse ({resource_group})
resource "azurerm_storage_account" "lakehouse_adls" {{
  name                     = "dfxlakehouseprod"
  resource_group_name      = "{resource_group}"
  location                 = "{location}"
  account_tier             = "Standard"
  account_replication_type = "GRS"
  is_hns_enabled           = true
}}
        """.strip()
        return hcl
