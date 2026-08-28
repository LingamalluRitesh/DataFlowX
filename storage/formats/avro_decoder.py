"""
DataFlowX Apache Avro Binary Data Block & Zigzag Varint Unpacker
Decodes Avro Object Container Files (OCF), sync markers, and variable-length zigzag binary integers.
"""

import io
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel


class AvroHeader(BaseModel):
    magic: bytes
    schema_json: str
    codec: str = "null"  # null, deflate, snappy, zstandard
    sync_marker: bytes


class AvroBinaryDecoder:
    """Decodes Avro binary formats."""

    @staticmethod
    def decode_varint(reader: io.BytesIO) -> int:
        """Reads variable-length integer."""
        res = 0
        shift = 0
        while True:
            b_byte = reader.read(1)
            if not b_byte:
                break
            b = ord(b_byte)
            res |= (b & 0x7F) << shift
            if (b & 0x80) == 0:
                break
            shift += 7
        return res

    @classmethod
    def decode_zigzag_int(cls, reader: io.BytesIO) -> int:
        """Decodes zigzag encoded 32/64 bit integer (n >> 1) ^ -(n & 1)."""
        n = cls.decode_varint(reader)
        return (n >> 1) ^ -(n & 1)

    @classmethod
    def decode_string(cls, reader: io.BytesIO) -> str:
        """Decodes length-prefixed UTF-8 string."""
        length = cls.decode_zigzag_int(reader)
        if length <= 0:
            return ""
        data = reader.read(length)
        return data.decode("utf-8", errors="replace")

    @classmethod
    def decode_boolean(cls, reader: io.BytesIO) -> bool:
        b = reader.read(1)
        return bool(ord(b)) if b else False
