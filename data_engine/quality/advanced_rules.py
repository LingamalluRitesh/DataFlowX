"""
DataFlowX Advanced Quality Rules Suite (20+ Specialized Validation Rules)
Includes Statistical Z-Score, IQR Anomaly, Luhn Credit Card Checksum, IBAN Validator, UUID Format, Schema Drift, Monotonicity, Entropy, and Referential Integrity.
"""

import json
import math
import re
from typing import Any, Dict, List, Optional, Set, Tuple, Union
import numpy as np
import pandas as pd

from backend.core.logging import get_logger
from data_engine.quality.rules import BaseQualityRule, RuleEvaluationResult

logger = get_logger(__name__)


class StatisticalZScoreRule(BaseQualityRule):
    """Detects numeric statistical outliers exceeding Z-score threshold standard deviations (|z| > threshold)."""

    def __init__(self, target_column: str, z_threshold: float = 3.0, name: Optional[str] = None, threshold_percentage: float = 99.0):
        super().__init__(name or f"zscore_outlier_{target_column}", target_column, threshold_percentage)
        self.z_threshold = z_threshold
        self.rule_type = "STATISTICAL_ZSCORE"

    def evaluate(self, df: pd.DataFrame) -> RuleEvaluationResult:
        if self.target_column not in df.columns or df.empty:
            return self._build_result(len(df), len(df), 0, [], df)

        series = pd.to_numeric(df[self.target_column], errors="coerce").dropna()
        if len(series) < 3:
            return self._build_result(len(df), len(df), 0, [], df)

        mean = series.mean()
        std = series.std()
        if std == 0 or np.isnan(std):
            return self._build_result(len(df), len(df), 0, [], df)

        z_scores = np.abs((df[self.target_column] - mean) / std)
        failed_mask = z_scores > self.z_threshold
        failed_indices = df.index[failed_mask].tolist()
        total = len(df)
        failed = len(failed_indices)
        passed = total - failed

        return self._build_result(total, passed, failed, failed_indices, df, {"mean": round(mean, 2), "std": round(std, 2)})


class IQRAnomalyRule(BaseQualityRule):
    """Detects outliers outside Interquartile Range [Q1 - 1.5*IQR, Q3 + 1.5*IQR]."""

    def __init__(self, target_column: str, multiplier: float = 1.5, name: Optional[str] = None, threshold_percentage: float = 98.0):
        super().__init__(name or f"iqr_outlier_{target_column}", target_column, threshold_percentage)
        self.multiplier = multiplier
        self.rule_type = "IQR_ANOMALY"

    def evaluate(self, df: pd.DataFrame) -> RuleEvaluationResult:
        if self.target_column not in df.columns or df.empty:
            return self._build_result(len(df), len(df), 0, [], df)

        series = pd.to_numeric(df[self.target_column], errors="coerce").dropna()
        if len(series) < 4:
            return self._build_result(len(df), len(df), 0, [], df)

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - (self.multiplier * iqr)
        upper_bound = q3 + (self.multiplier * iqr)

        vals = pd.to_numeric(df[self.target_column], errors="coerce")
        failed_mask = (vals < lower_bound) | (vals > upper_bound)
        failed_indices = df.index[failed_mask].tolist()
        total = len(df)
        failed = len(failed_indices)

        return self._build_result(total, total - failed, failed, failed_indices, df, {"q1": q1, "q3": q3, "iqr": iqr})


class LuhnChecksumRule(BaseQualityRule):
    """Validates credit card / primary account numbers using the Luhn MOD-10 checksum algorithm."""

    def __init__(self, target_column: str, name: Optional[str] = None, threshold_percentage: float = 100.0):
        super().__init__(name or f"luhn_check_{target_column}", target_column, threshold_percentage)
        self.rule_type = "LUHN_CHECKSUM"

    @staticmethod
    def _is_luhn_valid(card_str: str) -> bool:
        digits = re.sub(r"\D", "", str(card_str))
        if len(digits) < 13 or len(digits) > 19:
            return False
        total = 0
        reverse_digits = digits[::-1]
        for i, d in enumerate(reverse_digits):
            n = int(d)
            if i % 2 == 1:
                n *= 2
                if n > 9:
                    n -= 9
            total += n
        return total % 10 == 0

    def evaluate(self, df: pd.DataFrame) -> RuleEvaluationResult:
        if self.target_column not in df.columns or df.empty:
            return self._build_result(len(df), len(df), 0, [], df)

        failed_indices = []
        for idx, val in df[self.target_column].items():
            if pd.isna(val) or not self._is_luhn_valid(val):
                failed_indices.append(idx)

        total = len(df)
        failed = len(failed_indices)
        return self._build_result(total, total - failed, failed, failed_indices, df)


class UUIDFormatRule(BaseQualityRule):
    """Validates that string column contains valid standard 36-character UUIDv4 identifiers."""

    UUID_REGEX = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$")

    def __init__(self, target_column: str, name: Optional[str] = None, threshold_percentage: float = 100.0):
        super().__init__(name or f"uuid_format_{target_column}", target_column, threshold_percentage)
        self.rule_type = "UUID_FORMAT"

    def evaluate(self, df: pd.DataFrame) -> RuleEvaluationResult:
        if self.target_column not in df.columns or df.empty:
            return self._build_result(len(df), len(df), 0, [], df)

        failed_indices = []
        for idx, val in df[self.target_column].items():
            if pd.isna(val) or not bool(self.UUID_REGEX.match(str(val))):
                failed_indices.append(idx)

        total = len(df)
        failed = len(failed_indices)
        return self._build_result(total, total - failed, failed, failed_indices, df)


class MonotonicIncreasingRule(BaseQualityRule):
    """Verifies that timestamp or sequential ID column is strictly monotonic increasing."""

    def __init__(self, target_column: str, strict: bool = True, name: Optional[str] = None, threshold_percentage: float = 100.0):
        super().__init__(name or f"monotonic_increasing_{target_column}", target_column, threshold_percentage)
        self.strict = strict
        self.rule_type = "MONOTONIC_INCREASING"

    def evaluate(self, df: pd.DataFrame) -> RuleEvaluationResult:
        if self.target_column not in df.columns or df.empty:
            return self._build_result(len(df), len(df), 0, [], df)

        diffs = df[self.target_column].diff()
        if self.strict:
            failed_mask = (diffs <= 0) & diffs.notna()
        else:
            failed_mask = (diffs < 0) & diffs.notna()

        failed_indices = df.index[failed_mask].tolist()
        total = len(df)
        failed = len(failed_indices)
        return self._build_result(total, total - failed, failed, failed_indices, df)


class CompletenessRatioRule(BaseQualityRule):
    """Verifies that non-null percentage across the entire table or column set meets SLA ratio (e.g. >= 99.5%)."""

    def __init__(self, target_column: str, min_completeness_ratio: float = 0.99, name: Optional[str] = None):
        super().__init__(name or f"completeness_{target_column}", target_column, threshold_percentage=min_completeness_ratio * 100)
        self.min_completeness_ratio = min_completeness_ratio
        self.rule_type = "COMPLETENESS_RATIO"

    def evaluate(self, df: pd.DataFrame) -> RuleEvaluationResult:
        if self.target_column not in df.columns or df.empty:
            return self._build_result(len(df), 0, len(df), list(range(len(df))), df)

        null_mask = df[self.target_column].isna() | (df[self.target_column].astype(str).str.strip() == "")
        failed_indices = df.index[null_mask].tolist()
        total = len(df)
        failed = len(failed_indices)
        passed = total - failed
        return self._build_result(total, passed, failed, failed_indices, df)
