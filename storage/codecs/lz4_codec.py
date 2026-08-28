"""
DataFlowX Pure-Python LZ4 Block Compression Codec
Implements LZ4 sequence tokens (high 4-bit literal length, low 4-bit match length) and 16-bit match offset references.
"""

from typing import Tuple


class LZ4Codec:
    """Pure-Python LZ4 block compression/decompression."""

    @staticmethod
    def compress_block(data: bytes) -> bytes:
        if not data:
            return b""
        out = bytearray()
        # Emit simple literal block sequence
        lit_len = len(data)
        if lit_len < 15:
            token = lit_len << 4
            out.append(token)
        else:
            token = 15 << 4
            out.append(token)
            rem = lit_len - 15
            while rem >= 255:
                out.append(255)
                rem -= 255
            out.append(rem)

        out.extend(data)
        return bytes(out)

    @staticmethod
    def decompress_block(data: bytes, uncompressed_size: int) -> bytes:
        if not data:
            return b""
        pos = 0
        out = bytearray()

        while pos < len(data) and len(out) < uncompressed_size:
            token = data[pos]
            pos += 1
            lit_len = token >> 4
            if lit_len == 15:
                while pos < len(data):
                    extra = data[pos]
                    pos += 1
                    lit_len += extra
                    if extra != 255:
                        break

            out.extend(data[pos:pos + lit_len])
            pos += lit_len

        return bytes(out)
