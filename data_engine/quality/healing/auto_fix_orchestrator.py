"""
DataFlowX Automated Healing & Dead-Letter Queue (DLQ) Orchestrator
Quarantines unrecoverable invalid records into DLQ S3/Delta partitions while automatically repairing minor anomalies (imputation, clipping, trimming).
"""

from typing import Any, Dict, List, Optional, Tuple
import pandas as pd
from pydantic import BaseModel, Field

from backend.core.logging import get_logger
from data_engine.quality.healing.imputation import MissingValueImputer
from data_engine.quality.healing.outlier_clipper import OutlierClipper

logger = get_logger(__name__)


class HealingPlanSpec(BaseModel):
    impute_columns: Dict[str, str] = Field(default_factory=dict)  # col -> strategy
    clip_zscore_columns: Dict[str, float] = Field(default_factory=dict)  # col -> z_score
    quarantine_on_null: List[str] = Field(default_factory=list)


class HealingExecutionResult(BaseModel):
    healed_records_count: int
    quarantined_dlq_count: int
    clean_records_count: int
    dlq_destination: str = "s3://lakehouse/quarantine/dlq_failed_records/"


class AutoHealingOrchestrator:
    """Orchestrates automatic dataset repairs and DLQ isolation."""

    @classmethod
    def execute_healing(cls, df: pd.DataFrame, spec: HealingPlanSpec) -> Tuple[pd.DataFrame, pd.DataFrame, HealingExecutionResult]:
        if df.empty:
            return df, pd.DataFrame(), HealingExecutionResult(healed_records_count=0, quarantined_dlq_count=0, clean_records_count=0)

        working_df = df.copy()

        # 1. Isolate critical null records into DLQ
        dlq_mask = pd.Series([False] * len(working_df), index=working_df.index)
        for q_col in spec.quarantine_on_null:
            if q_col in working_df.columns:
                dlq_mask = dlq_mask | working_df[q_col].isna()

        dlq_df = working_df[dlq_mask].copy()
        clean_df = working_df[~dlq_mask].copy()

        # 2. Impute non-critical nulls
        for col, strat in spec.impute_columns.items():
            if col in clean_df.columns:
                clean_df = MissingValueImputer.impute_column(clean_df, col, strategy=strat)

        # 3. Clip extreme outliers
        for col, z_lim in spec.clip_zscore_columns.items():
            if col in clean_df.columns:
                clean_df = OutlierClipper.clip_zscore(clean_df, col, max_zscore=z_lim)

        result = HealingExecutionResult(
            healed_records_count=len(clean_df),
            quarantined_dlq_count=len(dlq_df),
            clean_records_count=len(clean_df)
        )

        logger.info(f"Auto-healing finished: {len(clean_df)} healed/cleaned, {len(dlq_df)} quarantined to DLQ")
        return clean_df, dlq_df, result
