"""
DataFlowX Column-Level Lineage & SQL Expression Dependency Graph
Parses transformation expressions and SQL queries to construct fine-grained column-level provenance graphs.
"""

from typing import Any, Dict, List, Optional, Set, Tuple
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class ColumnLineageEdge(BaseModel):
    source_table: str
    source_column: str
    target_table: str
    target_column: str
    transformation_expression: Optional[str] = None
    transformation_type: str = "DIRECT"  # DIRECT, RENAME, DERIVED, AGGREGATE, PASSTHROUGH


class ColumnLineageGraph(BaseModel):
    nodes: List[Dict[str, Any]] = Field(default_factory=list)
    edges: List[ColumnLineageEdge] = Field(default_factory=list)


class ColumnLineageTracker:
    """Constructs column-level lineage from DAG task dependencies and transformation configurations."""

    def __init__(self):
        self.edges: List[ColumnLineageEdge] = []

    def record_direct_mapping(self, src_tbl: str, src_col: str, tgt_tbl: str, tgt_col: str) -> None:
        self.edges.append(ColumnLineageEdge(
            source_table=src_tbl,
            source_column=src_col,
            target_table=tgt_tbl,
            target_column=tgt_col,
            transformation_type="DIRECT" if src_col == tgt_col else "RENAME"
        ))

    def record_derived_column(self, src_tbl: str, src_cols: List[str], tgt_tbl: str, tgt_col: str, expression: str) -> None:
        for scol in src_cols:
            self.edges.append(ColumnLineageEdge(
                source_table=src_tbl,
                source_column=scol,
                target_table=tgt_tbl,
                target_column=tgt_col,
                transformation_expression=expression,
                transformation_type="DERIVED"
            ))

    def get_upstream_lineage(self, table_name: str, column_name: str) -> List[ColumnLineageEdge]:
        """Find all upstream root columns that flow into this column."""
        results = []
        queue = [(table_name, column_name)]
        visited = set()

        while queue:
            curr_tbl, curr_col = queue.pop(0)
            if (curr_tbl, curr_col) in visited:
                continue
            visited.add((curr_tbl, curr_col))

            for edge in self.edges:
                if edge.target_table == curr_tbl and edge.target_column == curr_col:
                    results.append(edge)
                    queue.append((edge.source_table, edge.source_column))
        return results

    def get_downstream_impact(self, table_name: str, column_name: str) -> List[ColumnLineageEdge]:
        """Find all downstream columns and reports that depend on this column."""
        results = []
        queue = [(table_name, column_name)]
        visited = set()

        while queue:
            curr_tbl, curr_col = queue.pop(0)
            if (curr_tbl, curr_col) in visited:
                continue
            visited.add((curr_tbl, curr_col))

            for edge in self.edges:
                if edge.source_table == curr_tbl and edge.source_column == curr_col:
                    results.append(edge)
                    queue.append((edge.target_table, edge.target_column))
        return results
