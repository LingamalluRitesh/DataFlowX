"""
DataFlowX Forward Migration & Rollback SQL Script Generator
Automatically synthesizes ALTER TABLE statements and reverse compensation rollback scripts based on SchemaDiffResult.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from data_engine.migration.schema_comparator import ColumnDiff, SchemaDiffResult


class MigrationScript(BaseModel):
    version: str
    description: str
    up_sql: List[str] = Field(default_factory=list)
    down_sql: List[str] = Field(default_factory=list)


class MigrationGenerator:
    """Generates UP and DOWN SQL migration DDLs from computed schema diffs."""

    @classmethod
    def generate_migration(cls, diff: SchemaDiffResult, dialect: str = "POSTGRES") -> MigrationScript:
        up_statements = []
        down_statements = []

        tbl = diff.table_name

        for diff_col in diff.altered_columns:
            if diff_col.change_type == "ADDED":
                up_statements.append(f'ALTER TABLE "{tbl}" ADD COLUMN "{diff_col.column_name}" {diff_col.new_type};')
                down_statements.append(f'ALTER TABLE "{tbl}" DROP COLUMN "{diff_col.column_name}";')
            elif diff_col.change_type == "DROPPED":
                up_statements.append(f'ALTER TABLE "{tbl}" DROP COLUMN "{diff_col.column_name}";')
                down_statements.append(f'ALTER TABLE "{tbl}" ADD COLUMN "{diff_col.column_name}" {diff_col.old_type};')
            elif diff_col.change_type == "TYPE_CHANGED":
                if dialect.upper() == "POSTGRES":
                    up_statements.append(f'ALTER TABLE "{tbl}" ALTER COLUMN "{diff_col.column_name}" TYPE {diff_col.new_type};')
                    down_statements.append(f'ALTER TABLE "{tbl}" ALTER COLUMN "{diff_col.column_name}" TYPE {diff_col.old_type};')
                else:
                    up_statements.append(f'ALTER TABLE "{tbl}" MODIFY COLUMN "{diff_col.column_name}" {diff_col.new_type};')
                    down_statements.append(f'ALTER TABLE "{tbl}" MODIFY COLUMN "{diff_col.column_name}" {diff_col.old_type};')

        return MigrationScript(
            version=f"v_{int(datetime.now(timezone.utc).timestamp()) if 'datetime' in locals() else '1_0'}",
            description=f"Auto-generated schema migration for table '{tbl}'",
            up_sql=up_statements,
            down_sql=down_statements
        )
