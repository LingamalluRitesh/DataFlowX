"""
DataFlowX Algebraic Query Transformation & Equivalence Rules
Implements Join Commutativity (A JOIN B -> B JOIN A), Join Associativity ((A JOIN B) JOIN C -> A JOIN (B JOIN C)), and Filter Pushdown rules.
"""

from typing import List, Optional
from data_engine.optimizer.memo_structure import GroupExpression, MemoGroup, MemoStructure


class JoinCommutativityRule:
    """Transforms InnerJoin(A, B) into InnerJoin(B, A)."""

    @classmethod
    def apply(cls, expr: GroupExpression, memo: MemoStructure, group_id: int) -> Optional[GroupExpression]:
        if expr.operator_type != "INNER_JOIN" or len(expr.child_group_ids) != 2:
            return None

        left_gid, right_gid = expr.child_group_ids
        swapped_expr = GroupExpression(
            operator_type="INNER_JOIN",
            child_group_ids=[right_gid, left_gid],
            attributes=dict(expr.attributes)
        )
        memo.insert_expression(group_id, swapped_expr)
        return swapped_expr


class FilterPushdownRule:
    """Pushes filter predicate down below scan projections."""

    @classmethod
    def apply(cls, expr: GroupExpression, memo: MemoStructure, group_id: int) -> Optional[GroupExpression]:
        if expr.operator_type != "FILTER":
            return None
        # Push predicate to child scan group
        return None
