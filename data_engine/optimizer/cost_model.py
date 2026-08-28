"""
DataFlowX Physical Operator Cost Estimation Model
Estimates CPU cycle cost, Disk I/O cost, Network serialization cost, and Memory footprint based on table statistics and selectivity factors.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class TableStatistics(BaseModel):
    table_name: str
    total_row_count: int
    total_byte_size: int
    column_distinct_counts: Dict[str, int] = Field(default_factory=dict)
    column_null_fractions: Dict[str, float] = Field(default_factory=dict)


class PlanCost(BaseModel):
    cpu_cost: float
    io_cost: float
    network_cost: float
    memory_cost: float
    total_cost: float


class QueryCostModel:
    """Computes execution costs for query plan nodes."""

    CPU_CYCLE_WEIGHT = 0.01
    IO_BYTE_WEIGHT = 0.10
    NETWORK_TRANSFER_WEIGHT = 0.50
    MEMORY_BYTE_WEIGHT = 0.001

    @classmethod
    def estimate_scan_cost(cls, stats: TableStatistics, projection_columns: List[str]) -> PlanCost:
        proj_ratio = len(projection_columns) / max(1, len(stats.column_distinct_counts) or 10)
        scanned_bytes = stats.total_byte_size * proj_ratio
        io_c = scanned_bytes * cls.IO_BYTE_WEIGHT
        cpu_c = stats.total_row_count * cls.CPU_CYCLE_WEIGHT
        total = io_c + cpu_c
        return PlanCost(cpu_cost=cpu_c, io_cost=io_c, network_cost=0.0, memory_cost=0.0, total_cost=round(total, 2))

    @classmethod
    def estimate_hash_join_cost(cls, build_rows: int, probe_rows: int) -> PlanCost:
        cpu_c = (build_rows * 2 + probe_rows) * cls.CPU_CYCLE_WEIGHT
        mem_c = build_rows * 64 * cls.MEMORY_BYTE_WEIGHT
        total = cpu_c + mem_c
        return PlanCost(cpu_cost=cpu_c, io_cost=0.0, network_cost=0.0, memory_cost=mem_c, total_cost=round(total, 2))

    @classmethod
    def estimate_sort_cost(cls, num_rows: int) -> PlanCost:
        if num_rows <= 1:
            return PlanCost(cpu_cost=0.0, io_cost=0.0, network_cost=0.0, memory_cost=0.0, total_cost=0.0)
        import math
        cpu_c = num_rows * math.log2(num_rows) * cls.CPU_CYCLE_WEIGHT
        mem_c = num_rows * 32 * cls.MEMORY_BYTE_WEIGHT
        total = cpu_c + mem_c
        return PlanCost(cpu_cost=cpu_c, io_cost=0.0, network_cost=0.0, memory_cost=mem_c, total_cost=round(total, 2))
