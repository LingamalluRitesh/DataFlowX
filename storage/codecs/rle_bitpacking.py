"""
DataFlowX Parquet RLE & Bit-Packing Hybrid Codec
Encodes definition levels (NULL / Present) and repetition levels into hybrid Run-Length Encoded (RLE) and 1-bit to 8-bit packed streams.
"""

from typing import List


class RLEBitPackingHybridCodec:
    """Parquet RLE/Bit-packing encoder and decoder."""

    @staticmethod
    def encode_booleans_to_bitpacking(values: List[bool]) -> bytes:
        """Packs boolean list into byte array (8 booleans per byte)."""
        out = bytearray()
        curr_byte = 0
        bit_idx = 0

        for val in values:
            if val:
                curr_byte |= (1 << bit_idx)
            bit_idx += 1
            if bit_idx == 8:
                out.append(curr_byte)
                curr_byte = 0
                bit_idx = 0

        if bit_idx > 0:
            out.append(curr_byte)

        return bytes(out)

    @staticmethod
    def decode_bitpacking_to_booleans(data: bytes, total_count: int) -> List[bool]:
        """Unpacks byte array into boolean list."""
        out = []
        for b in data:
            for i in range(8):
                if len(out) < total_count:
                    out.append(bool((b >> i) & 1))
                else:
                    break
        return out
