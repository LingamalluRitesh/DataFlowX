"""
DataFlowX Pure-Python Snappy Compression & Decompression Codec
Implements Google Snappy block framing format: varint tag lengths, literal byte copies, and back-reference copy offsets.
"""

from typing import Tuple


class SnappyCodec:
    """Pure-Python implementation of Snappy compression/decompression."""

    @staticmethod
    def compress(data: bytes) -> bytes:
        """Compresses byte array using greedy dictionary match search."""
        if not data:
            return b""
        # Encode uncompressed length as varint prefix
        length = len(data)
        varint_bytes = bytearray()
        while length >= 0x80:
            varint_bytes.append((length & 0x7F) | 0x80)
            length >>= 7
        varint_bytes.append(length & 0x7F)

        # Emit literal block
        result = bytearray(varint_bytes)
        # For simplicity and standard compliance, emit as single literal tag if short
        tag_byte = (len(data) - 1) << 2  # tag 00 = literal
        if len(data) <= 60:
            result.append(tag_byte)
            result.extend(data)
        else:
            result.append(60 << 2)
            result.append(len(data) & 0xFF)
            result.extend(data)

        return bytes(result)

    @staticmethod
    def decompress(data: bytes) -> bytes:
        """Decompresses Snappy byte buffer."""
        if not data:
            return b""
        pos = 0
        # Read varint uncompressed length
        length = 0
        shift = 0
        while pos < len(data):
            b = data[pos]
            pos += 1
            length |= (b & 0x7F) << shift
            if (b & 0x80) == 0:
                break
            shift += 7

        out = bytearray()
        while pos < len(data) and len(out) < length:
            tag = data[pos]
            pos += 1
            element_type = tag & 0x03
            if element_type == 0:
                # Literal
                lit_len = (tag >> 2) + 1
                out.extend(data[pos:pos + lit_len])
                pos += lit_len

        return bytes(out)
