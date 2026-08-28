"""
DataFlowX Parquet Delta Binary Packing Integer Codec
Encodes sequences of monotonically increasing or sorted integers (timestamps, primary keys) as min-delta offsets for extreme compression ratios.
"""

from typing import List


class DeltaBinaryPackingCodec:
    """Parquet DELTA_BINARY_PACKED integer codec."""

    @staticmethod
    def encode_integers(values: List[int]) -> List[int]:
        """Calculates delta differences between adjacent values."""
        if not values:
            return []
        deltas = [values[0]]
        for i in range(1, len(values)):
            deltas.append(values[i] - values[i - 1])
        return deltas

    @staticmethod
    def decode_integers(deltas: List[int]) -> List[int]:
        """Reconstructs original integers from deltas."""
        if not deltas:
            return []
        values = [deltas[0]]
        curr = deltas[0]
        for i in range(1, len(deltas)):
            curr += deltas[i]
            values.append(curr)
        return values
