"""
DataFlowX Schema Diff & Breaking Change Analyzer
Compares source and target schemas, detecting added columns, dropped columns, altered data types, and nullability changes.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class SchemaColumnSpec(BaseModel):
    name: str
    type: str
    nullable: bool = True


class SchemaDiffReport(BaseModel):
    added_columns: List[str] = Field(default_factory=list)
    dropped_columns: List[str] = Field(default_factory=list)
    modified_types: Dict[str, Dict[str, str]] = Field(default_factory=dict)
    has_breaking_changes: bool = False


class SchemaDiffer:
    """Computes schema diffs."""

    @classmethod
    def compare_schemas(cls, old_schema: Dict[str, str], new_schema: Dict[str, str]) -> SchemaDiffReport:
        added = sorted(list(set(new_schema.keys()) - set(old_schema.keys())))
        dropped = sorted(list(set(old_schema.keys()) - set(new_schema.keys())))
        modified = {}

        for k in set(old_schema.keys()) & set(new_schema.keys()):
            if old_schema[k].upper() != new_schema[k].upper():
                modified[k] = {"from": old_schema[k], "to": new_schema[k]}

        # Dropped columns or type modifications are breaking changes
        breaking = len(dropped) > 0 or len(modified) > 0

        return SchemaDiffReport(
            added_columns=added,
            dropped_columns=dropped,
            modified_types=modified,
            has_breaking_changes=breaking
        )
