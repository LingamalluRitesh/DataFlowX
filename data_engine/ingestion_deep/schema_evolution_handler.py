"""
DataFlowX Automatic CDC Schema Evolution DDL Generator
Detects new columns in incoming change data capture streams and generates non-destructive `ALTER TABLE ... ADD COLUMN` DDL statements for Lakehouse targets.
"""

from typing import Dict, List, Set
from backend.core.logging import get_logger

logger = get_logger(__name__)


class CDCSchemaEvolutionHandler:
    """Detects schema drift and produces DDL statements."""

    @classmethod
    def detect_and_evolve_ddl(cls, table_name: str, existing_columns: Set[str], incoming_row: Dict[str, Any]) -> List[str]:
        new_cols = set(incoming_row.keys()) - existing_columns
        ddls = []
        for col in sorted(new_cols):
            val = incoming_row[col]
            sql_type = "BIGINT" if isinstance(val, int) else "DOUBLE" if isinstance(val, float) else "BOOLEAN" if isinstance(val, bool) else "STRING"
            ddl = f"ALTER TABLE {table_name} ADD COLUMN {col} {sql_type};"
            ddls.append(ddl)
            logger.info(f"Generated CDC schema evolution DDL: {ddl}")

        return ddls
