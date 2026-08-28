"""
DataFlowX Dynamic SQL Row-Level Security (RLS) Predicate Injector
Injects row-filtering WHERE clauses into user queries based on tenant isolation, user department, and country clearance tags.
"""

from typing import Dict, List, Optional
import pandas as pd
from pydantic import BaseModel, Field


class RowFilterPolicy(BaseModel):
    table_name: str
    tenant_column: str = "tenant_id"
    department_column: Optional[str] = "department"
    country_column: Optional[str] = "country"


class RowLevelFilterEngine:
    """Applies RLS predicates to queries and DataFrames."""

    @classmethod
    def apply_dataframe_rls(
        cls,
        df: pd.DataFrame,
        user_tenant_id: str,
        user_allowed_departments: Optional[List[str]] = None,
        user_country: Optional[str] = None
    ) -> pd.DataFrame:
        if df.empty:
            return df
        filtered = df.copy()

        if "tenant_id" in filtered.columns:
            filtered = filtered[filtered["tenant_id"] == user_tenant_id]

        if user_allowed_departments and "department" in filtered.columns:
            filtered = filtered[filtered["department"].isin(user_allowed_departments)]

        if user_country and "country" in filtered.columns:
            filtered = filtered[filtered["country"] == user_country]

        return filtered.reset_index(drop=True)
