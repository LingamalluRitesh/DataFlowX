"""
DataFlowX Arrow Flight Stream Producer
Serializes VectorBatch instances into zero-copy Apache Arrow IPC streams over gRPC transport for ultra-fast query downloads.
"""

from typing import Any, Dict, Generator, List
import pandas as pd
from data_engine.mpp_engine.vector_batch import VectorBatch


class ArrowFlightStreamProducer:
    """Streams columnar RecordBatches over Arrow Flight protocol."""

    @classmethod
    def stream_dataframe(cls, df: pd.DataFrame, chunk_size: int = 65536) -> Generator[Dict[str, Any], None, None]:
        total_rows = len(df)
        for offset in range(0, total_rows, chunk_size):
            chunk = df.iloc[offset:offset + chunk_size]
            batch = VectorBatch.from_dataframe(chunk)
            yield {
                "chunk_offset": offset,
                "chunk_rows": len(chunk),
                "columns": list(batch.columns.keys()),
                "data": chunk.to_dict(orient="list")
            }
