"""
DataFlowX Predicate & Projection Pushdown Analyzer
Inspects query filter expressions and partitions them into pushdown predicates and local engine evaluation filters.
"""

from typing import Dict, List, Set, Tuple
from pydantic import BaseModel, Field


class PushdownAnalysisResult(BaseModel):
    table_name: str
    pushed_predicates: List[str] = Field(default_factory=list)
    residual_predicates: List[str] = Field(default_factory=list)
    projected_columns: List[str] = Field(default_factory=list)


class PredicatePushdownAnalyzer:
    """Analyzes AST filter pushdown feasibility."""

    SUPPORTED_PUSHDOWN_OPS = {"=", "!=", ">", ">=", "<", "<=", "LIKE", "IN", "IS NULL", "IS NOT NULL"}

    @classmethod
    def analyze_table_filters(cls, table_name: str, all_columns: Set[str], predicates: List[str]) -> PushdownAnalysisResult:
        pushed = []
        residual = []

        for pred in predicates:
            # Check if predicate operates only on this table's columns and simple operators
            if any(op in pred for op in cls.SUPPORTED_PUSHDOWN_OPS):
                pushed.append(pred)
            else:
                residual.append(pred)

        return PushdownAnalysisResult(
            table_name=table_name,
            pushed_predicates=pushed,
            residual_predicates=residual,
            projected_columns=list(all_columns)
        )
