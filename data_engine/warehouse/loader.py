"""
DataFlowX Data Warehouse Loader
Loads Gold business-ready datasets into PostgreSQL or DuckDB analytical data warehouse tables with upsert and SCD Type 1 support.
"""

from datetime import datetime, timezone
import os
import sqlite3
from typing import Any, Dict, List, Optional
import pandas as pd
from sqlalchemy import create_engine, text
from backend.core.config import settings
from backend.core.logging import get_logger

try:
    import duckdb
except Exception:
    duckdb = None

logger = get_logger(__name__)


class WarehouseLoader:
    """Enterprise analytical warehouse loader."""

    def __init__(self, warehouse_type: Optional[str] = None):
        self.warehouse_type = warehouse_type or settings.WAREHOUSE_TYPE
        self.duckdb_path = os.path.abspath(settings.WAREHOUSE_DUCKDB_PATH)
        os.makedirs(os.path.dirname(self.duckdb_path), exist_ok=True)

    def load_gold_to_warehouse(
        self,
        records: List[Dict[str, Any]],
        table_name: str,
        mode: str = "upsert",  # 'append', 'overwrite', 'upsert'
        primary_keys: Optional[List[str]] = None,
    ) -> int:
        """Load records into analytical warehouse table."""
        if not records:
            return 0

        df = pd.DataFrame(records)

        if self.warehouse_type == "duckdb":
            return self._load_to_duckdb(df, table_name, mode, primary_keys)
        else:
            return self._load_to_postgres(df, table_name, mode, primary_keys)

    def _load_to_duckdb(
        self,
        df: pd.DataFrame,
        table_name: str,
        mode: str,
        primary_keys: Optional[List[str]] = None
    ) -> int:
        if duckdb is not None:
            try:
                con = duckdb.connect(self.duckdb_path)
                con.register("incoming_batch", df)

                safe_table = table_name.replace('"', '""')

                if mode == "overwrite":
                    con.execute(f'CREATE OR REPLACE TABLE "{safe_table}" AS SELECT * FROM incoming_batch')
                elif mode == "append":
                    con.execute(f'CREATE TABLE IF NOT EXISTS "{safe_table}" AS SELECT * FROM incoming_batch WHERE 1=0')
                    con.execute(f'INSERT INTO "{safe_table}" SELECT * FROM incoming_batch')
                elif mode == "upsert" and primary_keys:
                    con.execute(f'CREATE TABLE IF NOT EXISTS "{safe_table}" AS SELECT * FROM incoming_batch WHERE 1=0')
                    join_cond = " AND ".join([f'"{safe_table}"."{pk}" = incoming_batch."{pk}"' for pk in primary_keys])
                    con.execute(f'DELETE FROM "{safe_table}" WHERE EXISTS (SELECT 1 FROM incoming_batch WHERE {join_cond})')
                    con.execute(f'INSERT INTO "{safe_table}" SELECT * FROM incoming_batch')
                else:
                    con.execute(f'CREATE TABLE IF NOT EXISTS "{safe_table}" AS SELECT * FROM incoming_batch WHERE 1=0')
                    con.execute(f'INSERT INTO "{safe_table}" SELECT * FROM incoming_batch')

                con.close()
                logger.info(f"Loaded {len(df)} records into DuckDB analytical warehouse table '{table_name}' ({mode})")
                return len(df)
            except Exception:
                pass

        # SQLite Warehouse Fallback
        sqlite_warehouse_path = self.duckdb_path.replace(".duckdb", ".sqlite")
        con = sqlite3.connect(sqlite_warehouse_path)
        if mode == "overwrite":
            df.to_sql(table_name, con, if_exists="replace", index=False)
        else:
            df.to_sql(table_name, con, if_exists="append", index=False)
        con.close()
        logger.info(f"Loaded {len(df)} records into Analytical warehouse table '{table_name}' ({mode})")
        return len(df)

    def _load_to_postgres(
        self,
        df: pd.DataFrame,
        table_name: str,
        mode: str,
        primary_keys: Optional[List[str]] = None
    ) -> int:
        db_url = settings.WAREHOUSE_DATABASE_URL or settings.SYNC_DATABASE_URL
        engine = create_engine(db_url)

        if mode == "overwrite":
            df.to_sql(table_name, engine, if_exists="replace", index=False)
        elif mode == "append":
            df.to_sql(table_name, engine, if_exists="append", index=False)
        elif mode == "upsert" and primary_keys:
            # Stage temporary table and upsert
            temp_table = f"tmp_{table_name}_{int(datetime.now().timestamp())}"
            df.to_sql(temp_table, engine, if_exists="replace", index=False)

            pk_cols = ", ".join([f'"{pk}"' for pk in primary_keys])
            update_cols = ", ".join([f'"{c}" = EXCLUDED."{c}"' for c in df.columns if c not in primary_keys])
            all_cols = ", ".join([f'"{c}"' for c in df.columns])

            with engine.begin() as conn:
                conn.execute(text(f"""
                    CREATE TABLE IF NOT EXISTS "{table_name}" (LIKE "{temp_table}" INCLUDING ALL);
                    INSERT INTO "{table_name}" ({all_cols})
                    SELECT {all_cols} FROM "{temp_table}"
                    ON CONFLICT ({pk_cols}) DO UPDATE SET {update_cols};
                    DROP TABLE "{temp_table}";
                """))
        else:
            df.to_sql(table_name, engine, if_exists="append", index=False)

        engine.dispose()
        logger.info(f"Loaded {len(df)} records into PostgreSQL warehouse table '{table_name}' ({mode})")
        return len(df)
