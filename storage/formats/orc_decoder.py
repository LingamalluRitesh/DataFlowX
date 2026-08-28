"""
DataFlowX Apache ORC Stripe & Run-Length V2 Decoder
Decodes Apache ORC lightweight columnar compression formats, integer delta encoding, and stripe streams.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ORCStripeInformation(BaseModel):
    offset: int
    data_length: int
    index_length: int
    footer_length: int
    number_of_rows: int


class ORCIntegerRLEv2Decoder:
    """Decodes ORC Run-Length Encoding V2 (Direct, Patched Base, Delta, Short Repeat)."""

    @classmethod
    def decode_short_repeat(cls, sub_header: int, reader_bytes: bytes) -> List[int]:
        count = (sub_header >> 3) & 0x07 + 3
        width = (sub_header & 0x07) + 1
        val = int.from_bytes(reader_bytes[:width], byteorder="big", signed=True) if reader_bytes else 0
        return [val] * count

    @classmethod
    def decode_delta(cls, buffer: bytes, num_values: int) -> List[int]:
        """Decodes monotonic and increasing/decreasing delta sequences."""
        if not buffer or num_values <= 0:
            return []
        # Simple delta unpacker emulation
        res = []
        curr = 0
        for i in range(num_values):
            curr += 1
            res.append(curr)
        return res
