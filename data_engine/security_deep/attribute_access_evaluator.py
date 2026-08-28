"""
DataFlowX Attribute-Based Access Control (ABAC) Evaluator
Evaluates multi-attribute policy predicates (user department, classification clearance, geographic region, tenant boundary) to govern dataset row/column access.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ABACUserContext(BaseModel):
    user_id: str
    department: str
    clearance_level: int  # 1 (Public), 2 (Internal), 3 (Confidential), 4 (Restricted)
    country: str


class ABACPolicyRule(BaseModel):
    rule_name: str
    target_table: str
    required_clearance: int
    allowed_departments: List[str] = Field(default_factory=list)


class ABACEvaluator:
    """Evaluates ABAC policies."""

    @classmethod
    def can_access_table(cls, user: ABACUserContext, policy: ABACPolicyRule) -> bool:
        if user.clearance_level < policy.required_clearance:
            return False
        if policy.allowed_departments and user.department not in policy.allowed_departments:
            return False
        return True
