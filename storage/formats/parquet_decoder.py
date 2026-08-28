"""
DataFlowX Parquet Binary Page & Dictionary Encoding Decoder
Implements RLE/Bit-packing hybrid unpacker, dictionary index resolver, and column chunk statistics extraction for Parquet V1/V2 pages.
"""

import io
import struct
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field


class ParquetColumnChunkMeta(BaseModel):
    column_name: str
    num_values: int
    total_uncompressed_size: int
    total_compressed_size: int
    encodings: List[str] = Field(default_factory=list)
    min_value: Optional[Any] = None
    max_value: Optional[Any] = None
    null_count: int = 0


class ParquetPageHeader(BaseModel):
    page_type: str  # DATA_PAGE, DICTIONARY_PAGE, DATA_PAGE_V2
    uncompressed_page_size: int
    compressed_page_size: int
    num_values: int


class ParquetDecoder:
    """Decodes low-level Parquet page streams."""

    @classmethod
    def decode_rle_bitpacked_hybrid(cls, buffer: bytes, bit_width: int, count: int) -> List[int]:
        """Decodes hybrid RLE / bit-packed integers."""
        if not buffer or bit_width == 0:
            return [0] * count

        results: List[int] = []
        reader = io.BytesIO(buffer)

        while len(results) < count and reader.tell() < len(buffer):
            # Read unsigned varint header
            header = 0
            shift = 0
            while True:
                b_byte = reader.read(1)
                if not b_byte:
                    break
                b = ord(b_byte)
                header |= (b & 0x7F) << shift
                if (b & 0x80) == 0:
                    break
                shift += 7

            if (header & 1) == 0:
                # RLE Run: count = header >> 1
                rle_count = header >> 1
                # Read value of width (bit_width + 7) // 8 bytes
                width_bytes = max(1, (bit_width + 7) // 8)
                val_bytes = reader.read(width_bytes)
                val = int.from_bytes(val_bytes, byteorder="little") if val_bytes else 0
                results.extend([val] * rle_count)
            else:
                # Bit-packed group: num_groups = header >> 1, each group has 8 values
                num_groups = header >> 1
                num_values = num_groups * 8
                total_bytes = (num_values * bit_width) // 8
                packed_bytes = reader.read(total_bytes)
                # Unpack bit-packed stream
                bit_pos = 0
                bit_mask = (1 << bit_width) - 1
                for _ in range(min(num_values, count - len(results))):
                    byte_idx = bit_pos // 8
                    offset = bit_pos % 8
                    if byte_idx < len(packed_bytes):
                        raw = int.from_bytes(packed_bytes[byte_idx:byte_idx + 4], byteorder="little")
                        val = (raw >> offset) & bit_mask
                        results.append(val)
                    bit_pos += bit_width

        return results[:count]

    @classmethod
    def resolve_dictionary_page(cls, indices: List[int], dictionary_values: List[Any]) -> List[Any]:
        """Maps decoded integer dictionary indices to actual values."""
        return [dictionary_values[i] if 0 <= i < len(dictionary_values) else None for i in indices]
