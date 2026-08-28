"""
DataFlowX Data Mesh Domain Architecture & Data Product Model
Implements Data Mesh principles: Domain ownership, Data as a Product, Federated computational governance, and Self-serve data platform.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class DataProductPort(BaseModel):
    port_id: str
    port_type: str  # INPUT, OUTPUT, CONTROL
    protocol: str  # REST, SQL, KAFKA, S3_PARQUET, DELTA
    endpoint_uri: str
    data_contract_id: Optional[str] = None


class DataProduct(BaseModel):
    id: str
    name: str
    domain: str  # Marketing, Sales, SupplyChain, CoreBanking
    owner_team: str
    description: str
    version: str = "1.0.0"
    sla_availability_pct: float = 99.9
    ports: List[DataProductPort] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)


class DataMeshRegistry:
    """Registry of domain-owned Data Products."""

    def __init__(self):
        self._products: Dict[str, DataProduct] = {}

    def register_product(self, product: DataProduct) -> DataProduct:
        self._products[product.id] = product
        return product

    def get_products_by_domain(self, domain: str) -> List[DataProduct]:
        return [p for p in self._products.values() if p.domain.lower() == domain.lower()]
