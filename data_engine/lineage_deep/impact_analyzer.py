"""
DataFlowX Column Impact & Root-Cause Blast Radius Analyzer
Performs upstream topological traversals for root-cause diagnosis and downstream impact traversals with blast radius scoring.
"""

from typing import Dict, List, Set
from pydantic import BaseModel, Field
from data_engine.lineage_deep.sql_lineage_parser import ColumnLineageEdge


class BlastRadiusReport(BaseModel):
    root_column: str
    impacted_tables: List[str] = Field(default_factory=list)
    impacted_columns: List[str] = Field(default_factory=list)
    blast_radius_score: float = 0.0


class LineageImpactAnalyzer:
    """Computes blast radius of column changes."""

    @classmethod
    def compute_blast_radius(cls, column_key: str, edges: List[ColumnLineageEdge]) -> BlastRadiusReport:
        impacted_cols = set()
        impacted_tbls = set()

        for e in edges:
            src_key = f"{e.source_table}.{e.source_column}"
            if src_key == column_key or e.source_column == column_key:
                impacted_cols.add(f"{e.target_table}.{e.target_column}")
                impacted_tbls.add(e.target_table)

        return BlastRadiusReport(
            root_column=column_key,
            impacted_tables=list(impacted_tbls),
            impacted_columns=list(impacted_cols),
            blast_radius_score=len(impacted_cols) * 1.5
        )
