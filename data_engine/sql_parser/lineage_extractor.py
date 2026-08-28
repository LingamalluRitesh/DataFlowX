"""
DataFlowX SQL Lineage Extractor
Extracts source-to-target column mappings from SQL CREATE TABLE AS SELECT (CTAS) and VIEW statements.
"""

import re
from typing import Any, Dict, List, Optional
from data_engine.governance.column_lineage import ColumnLineageEdge


class SQLLineageExtractor:
    """Extracts column lineage from SQL statements."""

    @staticmethod
    def extract_ctas_lineage(target_table: str, sql_query: str) -> List[ColumnLineageEdge]:
        edges = []
        # Find column aliases
        select_match = re.search(r"SELECT\s+(.*?)\s+FROM", sql_query, re.IGNORECASE | re.DOTALL)
        if select_match:
            raw_cols = select_match.group(1).split(",")
            for rc in raw_cols:
                rc = rc.strip()
                if not rc:
                    continue
                # Check AS
                as_parts = re.split(r"\s+AS\s+", rc, flags=re.IGNORECASE)
                if len(as_parts) == 2:
                    expr, target_col = as_parts[0].strip(), as_parts[1].strip()
                else:
                    parts = rc.split()
                    expr, target_col = parts[0], parts[-1]

                edges.append(ColumnLineageEdge(
                    source_table="source_table",
                    source_column=expr,
                    target_table=target_table,
                    target_column=target_col,
                    transformation_expression=expr,
                    transformation_type="DERIVED" if "(" in expr else "DIRECT"
                ))
        return edges
