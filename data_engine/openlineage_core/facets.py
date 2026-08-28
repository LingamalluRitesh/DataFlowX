"""
DataFlowX OpenLineage Standard Dataset & Run Facets
Defines OpenLineage standard JSON facet models: SchemaDatasetFacet, DataSourceDatasetFacet, ColumnLineageDatasetFacet, and OutputStatisticsOutputDatasetFacet.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class OpenLineageSchemaField(BaseModel):
    name: str
    type: str
    description: Optional[str] = None


class SchemaDatasetFacet(BaseModel):
    _producer: str = "https://github.com/LingamalluRitesh/DataFlowX"
    _schemaURL: str = "https://openlineage.io/spec/facets/1-0-0/SchemaDatasetFacet.json"
    fields: List[OpenLineageSchemaField] = Field(default_factory=list)


class DataSourceDatasetFacet(BaseModel):
    _producer: str = "https://github.com/LingamalluRitesh/DataFlowX"
    _schemaURL: str = "https://openlineage.io/spec/facets/1-0-0/DatasourceDatasetFacet.json"
    name: str
    uri: str


class OutputStatisticsOutputDatasetFacet(BaseModel):
    _producer: str = "https://github.com/LingamalluRitesh/DataFlowX"
    _schemaURL: str = "https://openlineage.io/spec/facets/1-0-0/OutputStatisticsOutputDatasetFacet.json"
    rowCount: int
    size: int
