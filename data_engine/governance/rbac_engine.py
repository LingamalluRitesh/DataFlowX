"""
DataFlowX Fine-Grained Attribute-Based Access Control (ABAC) & Dynamic Row-Level Security
Applies user entitlement policies: row-level security predicates (tenant_id = X) and column-level masking (mask if !role.has_pii_access).
"""

from typing import Any, Dict, List, Optional, Set
import pandas as pd
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class UserSecurityContext(BaseModel):
    user_id: str
    tenant_id: str
    roles: List[str] = Field(default_factory=list)
    has_pii_unmask_permission: bool = False


class DatasetSecurityPolicy(BaseModel):
    dataset_name: str
    tenant_column: Optional[str] = "tenant_id"
    pii_columns: List[str] = Field(default_factory=list)
    restricted_roles: List[str] = Field(default_factory=list)


class DynamicSecurityFilter:
    """Enforces row-level filtering and column-level masking on DataFrames based on caller security context."""

    @staticmethod
    def apply_security_filter(
        df: pd.DataFrame,
        context: UserSecurityContext,
        policy: DatasetSecurityPolicy
    ) -> pd.DataFrame:
        if df.empty:
            return df
        filtered_df = df.copy()

        # 1. Row-Level Security (Tenant Isolation)
        if policy.tenant_column and policy.tenant_column in filtered_df.columns:
            if "SUPER_ADMIN" not in context.roles:
                filtered_df = filtered_df[filtered_df[policy.tenant_column] == context.tenant_id].reset_index(drop=True)

        # 2. Column-Level Dynamic Masking
        if not context.has_pii_unmask_permission:
            for pii_col in policy.pii_columns:
                if pii_col in filtered_df.columns:
                    filtered_df[pii_col] = "********"

        return filtered_df
