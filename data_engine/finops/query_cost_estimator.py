"""
DataFlowX Query Cost & Cloud Billing Estimator
Estimates monetary query execution costs across BigQuery ($6.25/TB), Snowflake credits ($3.00/credit), and Athena ($5.00/TB scanned).
"""

from pydantic import BaseModel


class QueryCostEstimate(BaseModel):
    engine: str
    bytes_scanned: int
    estimated_usd: float
    optimization_savings_usd: float = 0.0


class FinOpsQueryCostEstimator:
    """Estimates dollar cost of analytical workloads."""

    @classmethod
    def estimate_bigquery_cost(cls, bytes_scanned: int) -> QueryCostEstimate:
        tb = bytes_scanned / (1024 ** 4)
        cost = tb * 6.25
        return QueryCostEstimate(engine="BigQuery", bytes_scanned=bytes_scanned, estimated_usd=round(cost, 4))

    @classmethod
    def estimate_athena_cost(cls, bytes_scanned: int) -> QueryCostEstimate:
        tb = bytes_scanned / (1024 ** 4)
        cost = tb * 5.00
        return QueryCostEstimate(engine="AWS Athena", bytes_scanned=bytes_scanned, estimated_usd=round(cost, 4))
