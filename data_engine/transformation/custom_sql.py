import sqlite3
from typing import Any, Dict, List, Optional
import pandas as pd
from backend.core.exceptions import ValidationError
from backend.core.logging import get_logger

try:
    import duckdb
except Exception:
    duckdb = None

logger = get_logger(__name__)


class CustomSQLTransformer:
    """Vectorized SQL transformation engine powered by DuckDB & SQLite."""

    def __init__(self, sql_query: str):
        self.sql_query = sql_query.strip()
        self._validate_query()

    def _validate_query(self) -> None:
        if not self.sql_query:
            raise ValidationError("SQL query cannot be empty")

        # Disallow DDL / destructive queries in transformation queries
        upper_q = self.sql_query.upper()
        forbidden_keywords = ("DROP ", "TRUNCATE ", "DELETE ", "ALTER ", "INSERT INTO", "GRANT ", "REVOKE ")
        for kw in forbidden_keywords:
            if kw in upper_q:
                raise ValidationError(f"Forbidden SQL operation '{kw.strip()}' in transformation query")

    def execute(
        self,
        primary_df: pd.DataFrame,
        additional_tables: Optional[Dict[str, pd.DataFrame]] = None
    ) -> pd.DataFrame:
        """
        Execute SQL query against primary DataFrame (registered as `input_data` or `source`)
        and any optional additional DataFrames.
        """
        if duckdb is not None:
            con = duckdb.connect(database=":memory:")
            try:
                con.register("input_data", primary_df)
                con.register("source", primary_df)
                con.register("df", primary_df)

                if additional_tables:
                    for tbl_name, tbl_df in additional_tables.items():
                        con.register(tbl_name, tbl_df)

                res_df = con.execute(self.sql_query).df()
                return res_df.where(pd.notnull(res_df), None)
            except Exception:
                pass
            finally:
                con.close()

        # SQLite in-memory fallback
        try:
            con = sqlite3.connect(":memory:")
            primary_df.to_sql("input_data", con, index=False)
            primary_df.to_sql("source", con, index=False)
            primary_df.to_sql("df", con, index=False)

            if additional_tables:
                for tbl_name, tbl_df in additional_tables.items():
                    tbl_df.to_sql(tbl_name, con, index=False)

            res_df = pd.read_sql_query(self.sql_query, con)
            con.close()
            return res_df.where(pd.notnull(res_df), None)
        except Exception as exc:
            logger.error(f"SQL execution error on query '{self.sql_query}': {exc}")
            raise ValidationError(f"SQL Transformation Error: {str(exc)}")
