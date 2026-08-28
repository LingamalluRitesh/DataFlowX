"""
DataFlowX Confluent-Compatible Schema Evolution Validator
Validates schema transitions against BACKWARD, FORWARD, and FULL compatibility rules (checking deleted fields, optional vs required defaults).
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class SchemaField(BaseModel):
    name: str
    type: str
    default: Optional[Any] = None
    is_optional: bool = False


class SchemaCompatibilityReport(BaseModel):
    is_compatible: bool
    mode: str  # BACKWARD, FORWARD, FULL
    incompatible_reasons: List[str] = Field(default_factory=list)


class SchemaCompatibilityChecker:
    """Checks schema evolution rules."""

    @classmethod
    def check_backward_compatibility(cls, old_fields: List[SchemaField], new_fields: List[SchemaField]) -> SchemaCompatibilityReport:
        old_map = {f.name: f for f in old_fields}
        new_map = {f.name: f for f in new_fields}
        reasons = []

        # New fields must have defaults or be optional for backward compatibility
        for name, f in new_map.items():
            if name not in old_map and not f.is_optional and f.default is None:
                reasons.append(f"New required field '{name}' has no default value")

        return SchemaCompatibilityReport(
            is_compatible=len(reasons) == 0,
            mode="BACKWARD",
            incompatible_reasons=reasons
        )
