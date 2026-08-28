"""
DataFlowX Vectorized MPP Query Engine Service
Manages parallel query fragment execution pipelines and VectorBatch memory allocations.
"""

from typing import Any, Dict, List, Optional, Tuple
import pandas as pd
from data_engine.mpp_engine.physical_operators import FilterExec, LimitExec, ProjectionExec
from data_engine.mpp_engine.query_coordinator import MPPQueryCoordinator, QueryExecutionProfile
from data_engine.mpp_engine.vector_batch import VectorBatch


class VectorizedMPPService:
    """Service layer for vectorized analytical queries."""

    def __init__(self):
        self.coordinator = MPPQueryCoordinator()

    def run_query(self, df: pd.DataFrame, filter_col: Optional[str] = None, filter_val: Optional[Any] = None) -> Tuple[pd.DataFrame, QueryExecutionProfile]:
        batch = VectorBatch.from_dataframe(df)

        class StaticScan:
            def execute(self):
                yield batch

        plan = StaticScan()
        if filter_col and filter_val is not None:
            plan = FilterExec(plan, filter_col, "=", filter_val)

        return self.coordinator.execute_plan("query_mpp_01", plan)
