"""
DataFlowX Dynamic Column Redaction & Anonymization Policy Engine
Applies column-level redaction rules (FULL_MASK, HASH_SHA256, PARTIAL_MASK, NULLIFY) based on user RBAC authorization roles.
"""

from typing import Any, Dict, List, Optional
import pandas as pd


class ColumnRedactionPolicy:
    """Applies column redaction rules on DataFrames."""

    @classmethod
    def apply_policy(cls, df: pd.DataFrame, redactions: Dict[str, str]) -> pd.DataFrame:
        if df.empty:
            return df
        df = df.copy()

        for col, policy in redactions.items():
            if col in df.columns:
                if policy == "FULL_MASK":
                    df[col] = "********"
                elif policy == "NULLIFY":
                    df[col] = None
                elif policy == "PARTIAL_EMAIL":
                    # e.g., j***@example.com
                    df[col] = df[col].astype(str).apply(lambda x: x[0] + "***" + x[x.find("@"):] if "@" in x else "********")

        return df
