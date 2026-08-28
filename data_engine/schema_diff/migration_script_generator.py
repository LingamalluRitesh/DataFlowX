"""
DataFlowX Idempotent SQL Schema Migration Script Generator
Generates forward (UP) and rollback (DOWN) migration DDL scripts based on detected schema diffs for Lakehouse tables.
"""

from typing import Dict, List
from data_engine.schema_diff.schema_differ import SchemaDiffReport


class MigrationScriptGenerator:
    """Generates UP and DOWN SQL migration DDLs."""

    @classmethod
    def generate_migration_ddl(cls, table_name: str, diff: SchemaDiffReport, new_schema_types: Dict[str, str]) -> Dict[str, List[str]]:
        up_scripts = []
        down_scripts = []

        for col in diff.added_columns:
            c_type = new_schema_types.get(col, "STRING")
            up_scripts.append(f"ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {col} {c_type};")
            down_scripts.append(f"ALTER TABLE {table_name} DROP COLUMN IF EXISTS {col};")

        for col in diff.dropped_columns:
            up_scripts.append(f"ALTER TABLE {table_name} DROP COLUMN IF EXISTS {col};")
            down_scripts.append(f"ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {col} STRING;")

        for col, change in diff.modified_types.items():
            up_scripts.append(f"ALTER TABLE {table_name} ALTER COLUMN {col} TYPE {change['to']};")
            down_scripts.append(f"ALTER TABLE {table_name} ALTER COLUMN {col} TYPE {change['from']};")

        return {"up": up_scripts, "down": down_scripts}
