"""
DataFlowX Contextual Table Row Chunker
Chunks structured tabular data (CSV/Markdown) by serializing each row alongside its schema headers for RAG context preservation.
"""

from typing import Any, Dict, List
import pandas as pd
from pydantic import BaseModel, Field


class TableRowChunk(BaseModel):
    chunk_index: int
    row_number: int
    serialized_context: str
    key_identifiers: Dict[str, Any] = Field(default_factory=dict)


class TableRowChunker:
    """Chunks tabular datasets with contextual headers."""

    @classmethod
    def chunk_dataframe(cls, df: pd.DataFrame, key_columns: List[str]) -> List[TableRowChunk]:
        if df.empty:
            return []

        chunks = []
        for i, row in df.iterrows():
            # Build key-value prose: "Field: value, Field2: value2"
            parts = [f"{col}: {val}" for col, val in row.items()]
            serialized = ", ".join(parts)
            key_dict = {k: row[k] for k in key_columns if k in row}

            chunks.append(TableRowChunk(
                chunk_index=len(chunks),
                row_number=int(i),
                serialized_context=serialized,
                key_identifiers=key_dict
            ))

        return chunks
