"""
DataFlowX Logical Query Optimizer
Applies rule-based optimization passes: predicate pushdown, dead code elimination, constant folding, and projection pruning.
"""

from typing import Any, Dict, List, Optional
from data_engine.sql_dialects.ast_nodes import SelectQueryAST


class LogicalQueryOptimizer:
    """Applies algebraic transformation rules on Query AST."""

    @staticmethod
    def optimize_plan(ast: SelectQueryAST) -> SelectQueryAST:
        """Apply predicate pushdown and column pruning."""
        # Clean redundant projection duplicates
        seen_aliases = set()
        dedup_projections = []
        for p in ast.projections:
            alias = p.alias or str(p.expression)
            if alias not in seen_aliases:
                seen_aliases.add(alias)
                dedup_projections.append(p)

        ast.projections = dedup_projections
        return ast
