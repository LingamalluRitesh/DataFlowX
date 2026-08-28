"""
DataFlowX OpenDataContract Specification (ODCS v3.0) DSL Parser
Parses declarative YAML/JSON data contracts defining schema types, SLAs, data quality assertions, and tenant authorization.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ContractFieldSpec(BaseModel):
    name: str
    data_type: str
    required: bool = True
    unique: bool = False
    pii: bool = False
    min_value: Optional[float] = None
    max_value: Optional[float] = None


class ContractSLASpec(BaseModel):
    max_freshness_minutes: int = 60
    min_availability_pct: float = 99.9
    min_quality_score: float = 95.0


class DataContractSpecV2(BaseModel):
    contract_id: str
    dataset_name: str
    version: str = "v3.0.0"
    owner_team: str
    schema_fields: List[ContractFieldSpec] = Field(default_factory=list)
    sla: ContractSLASpec = Field(default_factory=ContractSLASpec)


class DataContractDSLParser:
    """Parses ODCS YAML/dict structures."""

    @classmethod
    def parse_contract_dict(cls, data: Dict[str, Any]) -> DataContractSpecV2:
        fields = []
        for f in data.get("schema", []):
            fields.append(ContractFieldSpec(
                name=f.get("name", ""),
                data_type=f.get("type", "STRING"),
                required=f.get("required", True),
                unique=f.get("unique", False),
                pii=f.get("pii", False),
                min_value=f.get("min"),
                max_value=f.get("max")
            ))

        sla_data = data.get("sla", {})
        sla = ContractSLASpec(
            max_freshness_minutes=sla_data.get("freshness_minutes", 60),
            min_availability_pct=sla_data.get("availability_pct", 99.9),
            min_quality_score=sla_data.get("min_quality_score", 95.0)
        )

        return DataContractSpecV2(
            contract_id=data.get("id", "contract_default"),
            dataset_name=data.get("dataset", ""),
            version=data.get("version", "v3.0.0"),
            owner_team=data.get("owner", "data-team"),
            schema_fields=fields,
            sla=sla
        )
