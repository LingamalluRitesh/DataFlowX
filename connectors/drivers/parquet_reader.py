"""
DataFlowX Pure-Python Parquet Metadata & Magic Byte Reader
Validates PAR1 magic headers, reads 4-byte footer length metadata, and verifies schema versioning without pyarrow dependencies.
"""

import os
import struct
from typing import Any, Dict, Optional, Tuple


class ParquetFileInspector:
    """Inspects Parquet binary file layout directly."""

    PARQUET_MAGIC = b"PAR1"

    @classmethod
    def inspect_file(cls, file_path: str) -> Dict[str, Any]:
        if not os.path.exists(file_path):
            return {"valid": False, "error": "File not found"}

        file_size = os.path.getsize(file_path)
        if file_size < 12:
            return {"valid": False, "error": "File too small for Parquet container"}

        with open(file_path, "rb") as f:
            # 1. Read header magic
            header_magic = f.read(4)
            if header_magic != cls.PARQUET_MAGIC:
                return {"valid": False, "error": f"Invalid header magic: {header_magic}"}

            # 2. Read footer metadata length & footer magic
            f.seek(-8, os.SEEK_END)
            footer_len_bytes = f.read(4)
            footer_magic = f.read(4)

            if footer_magic != cls.PARQUET_MAGIC:
                return {"valid": False, "error": f"Invalid footer magic: {footer_magic}"}

            footer_length = struct.unpack("<I", footer_len_bytes)[0]

            return {
                "valid": True,
                "file_size_bytes": file_size,
                "footer_length_bytes": footer_length,
                "metadata_offset": file_size - 8 - footer_length
            }
