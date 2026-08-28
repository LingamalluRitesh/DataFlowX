"""
DataFlowX Cascades Memo Graph & Equivalence Classes
Maintains equivalence classes (Group IDs) and GroupExpressions to represent the exponential search space of equivalent SQL plans compactly in polynomial memory.
"""

from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field


class GroupExpression(BaseModel):
    operator_type: str  # SCAN, FILTER, JOIN, AGGREGATE, SORT
    child_group_ids: List[int] = Field(default_factory=list)
    attributes: Dict[str, Any] = Field(default_factory=dict)
    estimated_cost: float = float("inf")


class MemoGroup(BaseModel):
    group_id: int
    expressions: List[GroupExpression] = Field(default_factory=list)
    best_expression: Optional[GroupExpression] = None
    best_cost: float = float("inf")


class MemoStructure:
    """Cascades memo container representing search space."""

    def __init__(self):
        self.groups: Dict[int, MemoGroup] = {}
        self._group_counter = 0

    def new_group(self) -> MemoGroup:
        gid = self._group_counter
        self._group_counter += 1
        group = MemoGroup(group_id=gid)
        self.groups[gid] = group
        return group

    def insert_expression(self, group_id: int, expr: GroupExpression) -> GroupExpression:
        group = self.groups[group_id]
        group.expressions.append(expr)
        return expr
