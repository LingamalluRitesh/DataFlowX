"""
DataFlowX Storage & Compute Cost Optimization Advisor
Estimates data warehouse query costs (Snowflake credits, BigQuery TB scanned, AWS S3 API charges), identifies uncompressed tables, and suggests partition key pruning.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class CostOptimizationRecommendation(BaseModel):
    category: str  # STORAGE, COMPUTE, NETWORK, RETENTION
    dataset_or_table: str
    estimated_monthly_savings_usd: float
    title: str
    description: str
    impact_level: str = "MEDIUM"  # LOW, MEDIUM, HIGH


class CostOptimizer:
    """Analyzes pipeline storage and query telemetry to generate actionable cost optimization recommendations."""

    @staticmethod
    def analyze_dataset_storage(
        dataset_name: str,
        size_bytes: int,
        format_type: str = "csv",
        monthly_query_count: int = 100
    ) -> List[CostOptimizationRecommendation]:
        recs = []
        size_gb = size_bytes / (1024 ** 3)

        # 1. Uncompressed format check
        if format_type.lower() in ("csv", "json") and size_gb > 1.0:
            savings = round(size_gb * 0.75 * 0.023, 2)  # S3 standard ~0.023 / GB
            recs.append(CostOptimizationRecommendation(
                category="STORAGE",
                dataset_or_table=dataset_name,
                estimated_monthly_savings_usd=savings,
                title="Convert uncompressed CSV/JSON to Parquet with Snappy",
                description=f"Converting '{dataset_name}' ({size_gb:.1f} GB) to columnar Parquet will reduce storage by ~75% and speed up query scans.",
                impact_level="HIGH"
            ))

        # 2. Partitioning recommendation
        if size_gb > 10.0 and monthly_query_count > 500:
            recs.append(CostOptimizationRecommendation(
                category="COMPUTE",
                dataset_or_table=dataset_name,
                estimated_monthly_savings_usd=round(monthly_query_count * 0.05, 2),
                title="Add date partitioning to reduce warehouse query scan cost",
                description=f"Adding partition key on date column for '{dataset_name}' avoids full table scans during incremental ETL runs.",
                impact_level="HIGH"
            ))

        return recs
