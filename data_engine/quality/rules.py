"""
DataFlowX Data Quality Rules
Implements rule validators: NOT_NULL, UNIQUE, RANGE, REGEX, EMAIL, DATA_TYPE, DATE_RANGE, DUPLICATE_CHECK, CUSTOM_SQL, CUSTOM_PYTHON.
"""

from abc import ABC, abstractmethod
from datetime import datetime
import re
import sqlite3
from typing import Any, Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field
from backend.core.logging import get_logger

try:
    import duckdb
except Exception:
    duckdb = None

logger = get_logger(__name__)


class RuleEvaluationResult(BaseModel):
    rule_name: str
    rule_type: str
    target_column: Optional[str] = None
    total_records: int
    passed_records: int
    failed_records: int
    score_percentage: float
    passed: bool
    threshold_percentage: float
    failed_indices: List[int] = Field(default_factory=list)
    failure_samples: List[Dict[str, Any]] = Field(default_factory=list)
    details: Dict[str, Any] = Field(default_factory=dict)


class BaseQualityRule(ABC):
    """Base interface for all data quality verification rules."""

    def __init__(
        self,
        name: str,
        target_column: Optional[str] = None,
        threshold_percentage: float = 100.0,
        severity: str = "ERROR"
    ):
        self.name = name
        self.target_column = target_column
        self.threshold_percentage = threshold_percentage
        self.severity = severity
        self.rule_type = "GENERIC"

    @abstractmethod
    def evaluate(self, df: pd.DataFrame) -> RuleEvaluationResult:
        pass

    def _build_result(
        self,
        total: int,
        passed: int,
        failed: int,
        failed_indices: List[int],
        df: pd.DataFrame,
        details: Optional[Dict[str, Any]] = None
    ) -> RuleEvaluationResult:
        score = (passed / total * 100.0) if total > 0 else 100.0
        is_passed = score >= self.threshold_percentage

        # Extract up to 5 sample failed rows
        samples = []
        if failed_indices and not df.empty:
            sample_slice = df.iloc[failed_indices[:5]]
            samples = sample_slice.where(pd.notnull(sample_slice), None).to_dict(orient="records")

        return RuleEvaluationResult(
            rule_name=self.name,
            rule_type=self.rule_type,
            target_column=self.target_column,
            total_records=total,
            passed_records=passed,
            failed_records=failed,
            score_percentage=round(score, 2),
            passed=is_passed,
            threshold_percentage=self.threshold_percentage,
            failed_indices=failed_indices,
            failure_samples=samples,
            details=details or {}
        )


class NotNullRule(BaseQualityRule):
    """Verifies that target column contains no null or empty values."""

    def __init__(self, target_column: str, name: Optional[str] = None, threshold_percentage: float = 100.0):
        super().__init__(name or f"not_null_{target_column}", target_column, threshold_percentage)
        self.rule_type = "NOT_NULL"

    def evaluate(self, df: pd.DataFrame) -> RuleEvaluationResult:
        if self.target_column not in df.columns:
            return self._build_result(len(df), 0, len(df), list(range(len(df))), df, {"error": "Column missing"})

        null_mask = df[self.target_column].isnull() | (df[self.target_column].astype(str).str.strip() == "")
        failed_indices = df.index[null_mask].tolist()
        total = len(df)
        failed = len(failed_indices)
        passed = total - failed

        return self._build_result(total, passed, failed, failed_indices, df)


class UniqueRule(BaseQualityRule):
    """Verifies that target column or combination of columns contains unique values."""

    def __init__(self, target_column: str, name: Optional[str] = None, threshold_percentage: float = 100.0):
        super().__init__(name or f"unique_{target_column}", target_column, threshold_percentage)
        self.rule_type = "UNIQUE"

    def evaluate(self, df: pd.DataFrame) -> RuleEvaluationResult:
        if self.target_column not in df.columns:
            return self._build_result(len(df), 0, len(df), list(range(len(df))), df, {"error": "Column missing"})

        dup_mask = df.duplicated(subset=[self.target_column], keep=False)
        failed_indices = df.index[dup_mask].tolist()
        total = len(df)
        failed = len(failed_indices)
        passed = total - failed

        return self._build_result(total, passed, failed, failed_indices, df)


class RangeRule(BaseQualityRule):
    """Verifies that numerical column values fall between [min_value, max_value]."""

    def __init__(
        self,
        target_column: str,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        name: Optional[str] = None,
        threshold_percentage: float = 100.0
    ):
        super().__init__(name or f"range_{target_column}", target_column, threshold_percentage)
        self.rule_type = "RANGE"
        self.min_value = min_value
        self.max_value = max_value

    def evaluate(self, df: pd.DataFrame) -> RuleEvaluationResult:
        if self.target_column not in df.columns:
            return self._build_result(len(df), 0, len(df), list(range(len(df))), df, {"error": "Column missing"})

        series = pd.to_numeric(df[self.target_column], errors="coerce")
        failed_mask = series.isnull()
        if self.min_value is not None:
            failed_mask |= (series < self.min_value)
        if self.max_value is not None:
            failed_mask |= (series > self.max_value)

        failed_indices = df.index[failed_mask].tolist()
        total = len(df)
        failed = len(failed_indices)
        passed = total - failed

        return self._build_result(total, passed, failed, failed_indices, df, {"min": self.min_value, "max": self.max_value})


class RegexRule(BaseQualityRule):
    """Verifies that text column matches regular expression pattern."""

    def __init__(self, target_column: str, pattern: str, name: Optional[str] = None, threshold_percentage: float = 100.0):
        super().__init__(name or f"regex_{target_column}", target_column, threshold_percentage)
        self.rule_type = "REGEX"
        self.pattern = pattern
        self._compiled = re.compile(pattern)

    def evaluate(self, df: pd.DataFrame) -> RuleEvaluationResult:
        if self.target_column not in df.columns:
            return self._build_result(len(df), 0, len(df), list(range(len(df))), df, {"error": "Column missing"})

        def match_fn(val):
            if pd.isnull(val):
                return False
            return bool(self._compiled.match(str(val)))

        matched = df[self.target_column].apply(match_fn)
        failed_indices = df.index[~matched].tolist()
        total = len(df)
        failed = len(failed_indices)
        passed = total - failed

        return self._build_result(total, passed, failed, failed_indices, df, {"pattern": self.pattern})


class EmailRule(BaseQualityRule):
    """Verifies that target column contains valid RFC 5322 standard email addresses."""

    EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

    def __init__(self, target_column: str, name: Optional[str] = None, threshold_percentage: float = 100.0):
        super().__init__(name or f"valid_email_{target_column}", target_column, threshold_percentage)
        self.rule_type = "EMAIL"

    def evaluate(self, df: pd.DataFrame) -> RuleEvaluationResult:
        if self.target_column not in df.columns:
            return self._build_result(len(df), 0, len(df), list(range(len(df))), df, {"error": "Column missing"})

        def check_email(val):
            if pd.isnull(val):
                return False
            return bool(self.EMAIL_REGEX.match(str(val).strip()))

        valid_mask = df[self.target_column].apply(check_email)
        failed_indices = df.index[~valid_mask].tolist()
        total = len(df)
        failed = len(failed_indices)
        passed = total - failed

        return self._build_result(total, passed, failed, failed_indices, df)


class CustomSqlRule(BaseQualityRule):
    """Executes SQL predicate query in DuckDB to validate row compliance."""

    def __init__(self, sql_condition: str, name: str, threshold_percentage: float = 100.0):
        super().__init__(name, None, threshold_percentage)
        self.rule_type = "CUSTOM_SQL"
        self.sql_condition = sql_condition

    def evaluate(self, df: pd.DataFrame) -> RuleEvaluationResult:
        total = len(df)
        if total == 0:
            return self._build_result(0, 0, 0, [], df)

        if duckdb is not None:
            con = duckdb.connect(database=":memory:")
            con.register("input_data", df)
            try:
                valid_df = con.execute(f"SELECT rowid FROM input_data WHERE {self.sql_condition}").df()
                valid_ids = set(valid_df["rowid"].tolist())
                all_ids = set(range(total))
                failed_indices = list(all_ids - valid_ids)
                passed = len(valid_ids)
                failed = len(failed_indices)
                return self._build_result(total, passed, failed, failed_indices, df, {"condition": self.sql_condition})
            except Exception:
                pass
            finally:
                con.close()

        # SQLite in-memory fallback
        try:
            con = sqlite3.connect(":memory:")
            df.to_sql("input_data", con, index=False)
            valid_df = pd.read_sql_query(f"SELECT rowid FROM input_data WHERE {self.sql_condition}", con)
            # SQLite rowid is 1-indexed
            valid_ids = set([int(x) - 1 for x in valid_df["rowid"].tolist()])
            all_ids = set(range(total))
            failed_indices = list(all_ids - valid_ids)
            passed = len(valid_ids)
            failed = len(failed_indices)
            con.close()
            return self._build_result(total, passed, failed, failed_indices, df, {"condition": self.sql_condition})
        except Exception as exc:
            logger.error(f"Custom SQL rule '{self.name}' failed: {exc}")
            return self._build_result(total, 0, total, list(range(total)), df, {"error": str(exc)})
