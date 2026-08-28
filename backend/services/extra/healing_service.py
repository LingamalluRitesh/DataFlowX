"""
DataFlowX Auto-Healing & Remediation Service Layer
Executes missing value imputation, outlier clipping, and Dead-Letter Queue (DLQ) isolation.
"""

from typing import Any, Dict, List, Optional, Tuple
import pandas as pd
from data_engine.quality.healing.auto_fix_orchestrator import AutoHealingOrchestrator, HealingExecutionResult, HealingPlanSpec


class HealingService:
    """Service layer for dataset auto-healing."""

    @classmethod
    def execute_dataset_healing(
        cls,
        df: pd.DataFrame,
        impute_map: Optional[Dict[str, str]] = None,
        quarantine_cols: Optional[List[str]] = None
    ) -> Tuple[pd.DataFrame, pd.DataFrame, HealingExecutionResult]:
        spec = HealingPlanSpec(
            impute_columns=impute_map or {},
            quarantine_on_null=quarantine_cols or []
        )
        return AutoHealingOrchestrator.execute_healing(df, spec)
