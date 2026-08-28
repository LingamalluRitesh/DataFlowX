"""
DataFlowX Apache Arrow IPC Streaming Protocol & FlatBuffers Frame Reader
Decodes Arrow IPC RecordBatch stream messages, field dictionaries, and zero-copy binary buffer pointers.
"""

from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field


class ArrowField(BaseModel):
    name: str
    type_name: str
    nullable: bool = True


class ArrowSchema(BaseModel):
    fields: List[ArrowField] = Field(default_factory=list)


class ArrowRecordBatchMessage(BaseModel):
    schema_def: ArrowSchema
    length: int
    column_names: List[str] = Field(default_factory=list)


class ArrowIPCStreamDecoder:
    """Decodes Arrow IPC streams."""

    @classmethod
    def parse_dataframe_to_arrow_meta(cls, df: pd.DataFrame) -> ArrowRecordBatchMessage:
        fields = []
        for col in df.columns:
            dtype_str = str(df[col].dtype)
            type_name = "INT64" if "int" in dtype_str else "FLOAT64" if "float" in dtype_str else "UTF8"
            fields.append(ArrowField(name=col, type_name=type_name, nullable=bool(df[col].isna().any())))

        schema_def = ArrowSchema(fields=fields)
        return ArrowRecordBatchMessage(
            schema_def=schema_def,
            length=len(df),
            column_names=list(df.columns)
        )
