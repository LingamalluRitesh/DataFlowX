"""
DataFlowX Deep Schema Comparator & Structural Diff Engine
Compares source and target table schemas to detect backward-incompatible breaking changes, added columns, dropped columns, and type widening/narrowing.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from data_engine.migration.ddl_parser import ParsedColumnDefinition, ParsedTableDDL


class ColumnDiff(BaseModel):
    column_name: str
    change_type: str  # ADDED, DROPPED, TYPE_CHANGED, NULLABILITY_CHANGED
    old_type: Optional[str] = None
    new_type: Optional[str] = None
    is_breaking_change: bool = False


class SchemaDiffResult(BaseModel):
    table_name: str
    has_changes: bool = False
    has_breaking_changes: bool = False
    added_columns: List[str] = Field(default_factory=list)
    dropped_columns: List[str] = Field(default_factory=list)
    altered_columns: List[ColumnDiff] = Field(default_factory=list)


class SchemaComparator:
    """Computes schema diffs between two table schemas."""

    @classmethod
    def compare_tables(cls, old_table: ParsedTableDDL, new_table: ParsedTableDDL) -> SchemaDiffResult:
        old_cols = {c.name.lower(): c for c in old_table.columns}
        new_cols = {c.name.lower(): c for c in new_table.columns}

        added = []
        dropped = []
        altered = []
        has_breaking = False

        # Check for added columns
        for name, col in new_cols.items():
            if name not in old_cols:
                added.append(col.name)
                altered.append(ColumnDiff(
                    column_name=col.name,
                    change_type="ADDED",
                    new_type=col.data_type,
                    is_breaking_change=not col.is_nullable  # Adding non-nullable column without default is breaking
                ))
                if not col.is_nullable:
                    has_breaking = True

        # Check for dropped columns
        for name, col in old_cols.items():
            if name not in new_cols:
                dropped.append(col.name)
                altered.append(ColumnDiff(
                    column_name=col.name,
                    change_type="DROPPED",
                    old_type=col.data_type,
                    is_breaking_change=True
                ))
                has_breaking = True

        # Check for modified columns
        for name in old_cols:
            if name in new_cols:
                old_c = old_cols[name]
                new_c = new_cols[name]
                if old_c.data_type.upper() != new_c.data_type.upper():
                    altered.append(ColumnDiff(
                        column_name=new_c.name,
                        change_type="TYPE_CHANGED",
                        old_type=old_c.data_type,
                        new_type=new_c.data_type,
                        is_breaking_change=True
                    ))
                    has_breaking = True

        has_changes = len(added) > 0 or len(dropped) > 0 or len(altered) > 0

        return SchemaDiffResult(
            table_name=new_table.table_name,
            has_changes=has_changes,
            has_breaking_changes=has_breaking,
            added_columns=added,
            dropped_columns=dropped,
            altered_columns=altered
        )
