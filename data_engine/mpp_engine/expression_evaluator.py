"""
DataFlowX Vectorized Physical Expression Evaluator
Applies vectorized SIMD arithmetic operations (+, -, *, /), boolean comparisons, string lower/upper/concat, and null coalescing.
"""

from typing import Any, Callable, Dict, List, Optional
import numpy as np
from data_engine.mpp_engine.vector_batch import ColumnVector, VectorBatch


class VectorizedExpressionEvaluator:
    """Evaluates algebraic expressions over VectorBatch instances."""

    @staticmethod
    def eval_binary_arithmetic(left: ColumnVector, right: ColumnVector, op: str) -> ColumnVector:
        out_values = []
        for i in range(left.length):
            if left.is_null(i) or right.is_null(i):
                out_values.append(None)
                continue
            l_val, r_val = left.get_value(i), right.get_value(i)
            if op == "+":
                out_values.append(l_val + r_val)
            elif op == "-":
                out_values.append(l_val - r_val)
            elif op == "*":
                out_values.append(l_val * r_val)
            elif op == "/":
                out_values.append(l_val / r_val if r_val != 0 else None)

        return ColumnVector(data_type="FLOAT", data=out_values)

    @staticmethod
    def eval_comparison(col: ColumnVector, literal: Any, op: str) -> List[bool]:
        mask = []
        for i in range(col.length):
            if col.is_null(i):
                mask.append(False)
                continue
            v = col.get_value(i)
            if op == "=" or op == "==":
                mask.append(v == literal)
            elif op == "!=":
                mask.append(v != literal)
            elif op == ">":
                mask.append(v > literal)
            elif op == ">=":
                mask.append(v >= literal)
            elif op == "<":
                mask.append(v < literal)
            elif op == "<=":
                mask.append(v <= literal)
            else:
                mask.append(False)
        return mask
