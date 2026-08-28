"""
DataFlowX Numerical Edge Case & Overflow Fuzzer
Injects NaN, ±Infinity, subnormal float representations, and boundary 64-bit integer values (2^63 - 1, -2^63) to verify SIMD vector stability.
"""

from typing import List, Union
import numpy as np


class NumericalFuzzer:
    """Generates numerical boundary values."""

    @classmethod
    def get_float_edge_cases(cls) -> List[float]:
        return [
            float("nan"),
            float("inf"),
            float("-inf"),
            0.0,
            -0.0,
            1e-300,  # Subnormal
            1.7976931348623157e+308,  # Max double
            -1.7976931348623157e+308  # Min double
        ]

    @classmethod
    def get_int64_edge_cases(cls) -> List[int]:
        return [
            0,
            -1,
            9223372036854775807,  # INT64_MAX
            -9223372036854775808,  # INT64_MIN
            2147483647,  # INT32_MAX
            -2147483648  # INT32_MIN
        ]
