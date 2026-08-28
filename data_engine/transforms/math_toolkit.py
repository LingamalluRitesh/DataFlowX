"""
DataFlowX Advanced Mathematics, Information Theory & Statistics Toolkit
Calculates Shannon Entropy, Gini Impurity, Kullback-Leibler (KL) Divergence, Logistic Sigmoid, and Softmax vector normalizations for feature engineering.
"""

import math
from typing import Any, List, Optional
import numpy as np
import pandas as pd


class MathToolkit:
    """Mathematical and information theoretic functions for data transformation."""

    @staticmethod
    def shannon_entropy(probabilities: List[float]) -> float:
        """Calculate Shannon entropy H(X) in bits."""
        ent = 0.0
        for p in probabilities:
            if p > 0.0:
                ent -= p * math.log2(p)
        return round(ent, 4)

    @staticmethod
    def gini_impurity(class_counts: List[int]) -> float:
        """Calculate Gini impurity for classification splitting."""
        total = sum(class_counts)
        if total == 0:
            return 0.0
        gini = 1.0 - sum((cnt / total) ** 2 for cnt in class_counts)
        return round(gini, 4)

    @staticmethod
    def sigmoid(x: float) -> float:
        """Logistic sigmoid function 1 / (1 + e^-x)."""
        return 1.0 / (1.0 + math.exp(-max(min(x, 100.0), -100.0)))

    @staticmethod
    def softmax(vector: List[float]) -> List[float]:
        """Compute Softmax probability distribution."""
        max_val = max(vector) if vector else 0.0
        exp_vals = [math.exp(v - max_val) for v in vector]
        sum_exp = sum(exp_vals)
        return [round(e / sum_exp, 6) for e in exp_vals] if sum_exp > 0 else []

    @classmethod
    def apply_sigmoid(cls, df: pd.DataFrame, col: str, output_col: Optional[str] = None) -> pd.DataFrame:
        if df.empty or col not in df.columns:
            return df
        df = df.copy()
        out = output_col or f"{col}_sigmoid"
        df[out] = pd.to_numeric(df[col], errors="coerce").apply(lambda v: cls.sigmoid(v) if pd.notna(v) else None)
        return df
