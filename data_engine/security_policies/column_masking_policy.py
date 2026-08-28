"""
DataFlowX Dynamic Column Masking Policy Engine
Applies column-level transformations (SHA-256 Hash, Partial Email Mask, Credit Card Last-4, Full Nullification) based on user role.
"""

import hashlib
from typing import Dict, List, Optional
import pandas as pd
from pydantic import BaseModel


class ColumnMaskRule(BaseModel):
    column_name: str
    mask_type: str  # HASH_SHA256, MASK_EMAIL, LAST_4_DIGITS, NULLIFY, FPE
    exempt_roles: List[str] = ["admin", "security_officer"]


class DynamicColumnMasker:
    """Applies column masking dynamically."""

    @classmethod
    def mask_dataframe(cls, df: pd.DataFrame, rules: List[ColumnMaskRule], user_role: str) -> pd.DataFrame:
        if df.empty:
            return df
        res = df.copy()

        for r in rules:
            if user_role in r.exempt_roles:
                continue
            if r.column_name not in res.columns:
                continue

            if r.mask_type == "HASH_SHA256":
                res[r.column_name] = res[r.column_name].astype(str).apply(
                    lambda x: hashlib.sha256(x.encode("utf-8")).hexdigest() if pd.notna(x) else None
                )
            elif r.mask_type == "MASK_EMAIL":
                def _mask_email(val):
                    if not isinstance(val, str) or "@" not in val:
                        return "***@***.com"
                    user, dom = val.split("@", 1)
                    return f"{user[:1]}***@{dom}"
                res[r.column_name] = res[r.column_name].apply(_mask_email)
            elif r.mask_type == "LAST_4_DIGITS":
                res[r.column_name] = res[r.column_name].astype(str).apply(
                    lambda x: f"****-****-****-{x[-4:]}" if len(x) >= 4 else "****"
                )
            elif r.mask_type == "NULLIFY":
                res[r.column_name] = None

        return res
