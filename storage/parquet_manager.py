"""
DataFlowX Parquet Storage & Serialization Manager
High-performance Parquet read/write manager using PyArrow and DuckDB with Snappy/ZSTD compression.
"""

import io
import os
from typing import Any, Dict, List, Optional, Union
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

try:
    import duckdb
except Exception:
    duckdb = None
from backend.core.exceptions import StorageError
from backend.core.logging import get_logger

logger = get_logger(__name__)


class ParquetManager:
    """Enterprise Parquet format serialization and partition manager."""

    @staticmethod
    def dataframe_to_parquet_bytes(
        df: pd.DataFrame,
        compression: str = "SNAPPY"
    ) -> bytes:
        """Convert a Pandas DataFrame directly to Parquet binary buffer."""
        table = pa.Table.from_pandas(df)
        buf = io.BytesIO()
        pq.write_table(table, buf, compression=compression)
        return buf.getvalue()

    @staticmethod
    def records_to_parquet_bytes(
        records: List[Dict[str, Any]],
        schema: Optional[pa.Schema] = None,
        compression: str = "SNAPPY"
    ) -> bytes:
        """Convert a list of dictionaries into compressed Parquet bytes."""
        if not records:
            # Return empty table bytes
            empty_table = pa.Table.from_pydict({})
            out_buf = io.BytesIO()
            pq.write_table(empty_table, out_buf, compression=compression)
            return out_buf.getvalue()

        df = pd.DataFrame(records)
        # Convert objects to string or json string if nested
        for col in df.columns:
            sample_val = df[col].dropna().iloc[0] if not df[col].dropna().empty else None
            if isinstance(sample_val, (dict, list)):
                import json
                df[col] = df[col].apply(lambda x: json.dumps(x) if x is not None else None)

        table = pa.Table.from_pandas(df, schema=schema, preserve_index=False)
        out_buf = io.BytesIO()
        pq.write_table(table, out_buf, compression=compression)
        return out_buf.getvalue()

    @staticmethod
    def parquet_bytes_to_records(data: bytes, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Parse raw Parquet bytes into a list of record dictionaries."""
        if not data:
            return []
        in_buf = io.BytesIO(data)
        table = pq.read_table(in_buf)
        df = table.to_pandas()
        if limit:
            df = df.head(limit)
        return df.where(pd.notnull(df), None).to_dict(orient="records")

    @staticmethod
    def write_parquet_file(
        records: List[Dict[str, Any]],
        file_path: str,
        compression: str = "SNAPPY",
        partition_cols: Optional[List[str]] = None,
    ) -> str:
        """Write record batch directly to a local Parquet file or partitioned directory."""
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        if not records:
            empty_df = pd.DataFrame()
            table = pa.Table.from_pandas(empty_df)
            pq.write_table(table, file_path, compression=compression)
            return file_path

        df = pd.DataFrame(records)
        table = pa.Table.from_pandas(df, preserve_index=False)

        if partition_cols:
            pq.write_to_dataset(
                table,
                root_path=file_path,
                partition_cols=partition_cols,
                compression=compression,
            )
        else:
            pq.write_table(table, file_path, compression=compression)

        return file_path

    @staticmethod
    def read_parquet_file(file_path: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Read records from local Parquet file."""
        if not os.path.exists(file_path):
            raise StorageError(f"Parquet file not found: {file_path}", path=file_path)

        table = pq.read_table(file_path)
        df = table.to_pandas()
        if limit:
            df = df.head(limit)
        return df.where(pd.notnull(df), None).to_dict(orient="records")

    @staticmethod
    def query_parquet_sql(file_or_glob_path: str, sql_query: str) -> List[Dict[str, Any]]:
        """Execute fast SQL query directly over Parquet files."""
        if duckdb is not None:
            try:
                con = duckdb.connect(database=":memory:")
                safe_path = file_or_glob_path.replace("'", "''")
                query = sql_query.replace("{{source}}", f"read_parquet('{safe_path}')")
                if "read_parquet" not in query:
                    query = f"SELECT * FROM read_parquet('{safe_path}')"

                res_df = con.execute(query).df()
                con.close()
                return res_df.where(pd.notnull(res_df), None).to_dict(orient="records")
            except Exception:
                pass

        # Robust Pandas + SQLite fallback
        recs = ParquetManager.read_parquet_file(file_or_glob_path)
        df = pd.DataFrame(recs)
        import sqlite3
        con = sqlite3.connect(":memory:")
        df.to_sql("input_data", con, index=False)
        clean_q = sql_query.replace("{{source}}", "input_data")
        res_df = pd.read_sql_query(clean_q, con)
        con.close()
        return res_df.where(pd.notnull(res_df), None).to_dict(orient="records")
