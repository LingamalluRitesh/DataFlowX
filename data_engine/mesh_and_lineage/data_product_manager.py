"""
DataFlowX Data Mesh Domain Product Lifecycle Manager
Defines decentralized Data Products with output ports, SLA health contracts, access control policies, and domain ownership.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class DataProductPort(BaseModel):
    port_id: str
    port_name: str
    protocol: str  # DELTA_SHARING, ARROW_FLIGHT, REST_API, ICEBERG_CATALOG
    endpoint_url: str
    schema_definition: Dict[str, str] = Field(default_factory=dict)
    is_active: bool = True


class DataProduct(BaseModel):
    product_id: str
    domain: str  # Finance, Marketing, SupplyChain, CustomerSuccess
    name: str
    description: str
    owner_team: str
    sla_freshness_minutes: int = 60
    input_ports: List[DataProductPort] = Field(default_factory=list)
    output_ports: List[DataProductPort] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = "PUBLISHED"  # DRAFT, PUBLISHED, DEPRECATED


class DataProductManager:
    """Manages Data Mesh data products across enterprise domains."""

    def __init__(self):
        self.products: Dict[str, DataProduct] = {}

    def register_product(self, product: DataProduct) -> DataProduct:
        self.products[product.product_id] = product
        return product

    def get_domain_products(self, domain: str) -> List[DataProduct]:
        return [p for p in self.products.values() if p.domain.lower() == domain.lower()]
