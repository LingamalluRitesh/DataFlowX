"""
DataFlowX GraphQL Selection-Set to Pushdown SQL Query Resolver
Translates incoming GraphQL nested selection sets into minimal SQL column projections and WHERE clauses.
"""

from typing import Any, Dict, List, Optional
import pandas as pd


class GraphQLQueryResolver:
    """Resolves GraphQL selection fields into SQL."""

    @classmethod
    def resolve_selection(cls, df: pd.DataFrame, requested_fields: List[str], filter_kwargs: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        if df.empty:
            return []
        working_df = df.copy()

        if filter_kwargs:
            for k, v in filter_kwargs.items():
                if k in working_df.columns:
                    working_df = working_df[working_df[k] == v]

        valid_fields = [f for f in requested_fields if f in working_df.columns]
        if not valid_fields:
            return []

        return working_df[valid_fields].to_dict(orient="records")
