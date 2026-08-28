"""
DataFlowX Fine-Grained Column-Level Lineage Builder
Constructs column-to-column dependency edges linking target columns to source columns through transformation expressions.
"""

from typing import Dict, List, Set
from pydantic import BaseModel, Field


class ColumnLineageEdge(BaseModel):
    source_table: str
    source_column: str
    target_table: str
    target_column: str
    transformation_type: str = "DIRECT_COPY"  # DIRECT_COPY, ARITHMETIC, AGGREGATION, CONDITIONAL


class ColumnLevelLineageGraph(BaseModel):
    edges: List[ColumnLineageEdge] = Field(default_factory=list)


class ColumnLineageBuilder:
    """Builds and analyzes column-level lineage graphs."""

    def __init__(self):
        self.edges: List[ColumnLineageEdge] = []

    def add_edge(self, source_table: str, source_col: str, target_table: str, target_col: str, transform_type: str = "DIRECT_COPY") -> None:
        edge = ColumnLineageEdge(
            source_table=source_table,
            source_column=source_col,
            target_table=target_table,
            target_column=target_col,
            transformation_type=transform_type
        )
        self.edges.append(edge)

    def get_source_columns_for_target(self, target_table: str, target_col: str) -> List[ColumnLineageEdge]:
        return [e for e in self.edges if e.target_table == target_table and e.target_column == target_col]
