"""
DataFlowX Confluent Avro CDC Wire Protocol Deserializer
Unpacks magic byte (0x00) and 4-byte big-endian Schema ID headers from Confluent Kafka CDC message payloads.
"""

import io
import struct
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel


class ConfluentAvroPayload(BaseModel):
    schema_id: int
    raw_payload_bytes: bytes


class ConfluentAvroDeserializer:
    """Deserializes Kafka message wire format headers."""

    MAGIC_BYTE = 0x00

    @classmethod
    def parse_wire_format(cls, message_bytes: bytes) -> Optional[ConfluentAvroPayload]:
        if len(message_bytes) < 5:
            return None

        # Byte 0: Magic byte
        magic = message_bytes[0]
        if magic != cls.MAGIC_BYTE:
            return None

        # Bytes 1-4: Schema ID (big-endian uint32)
        schema_id = struct.unpack(">I", message_bytes[1:5])[0]
        payload = message_bytes[5:]

        return ConfluentAvroPayload(
            schema_id=schema_id,
            raw_payload_bytes=payload
        )
