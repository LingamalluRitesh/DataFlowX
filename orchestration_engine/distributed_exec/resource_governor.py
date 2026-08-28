"""
DataFlowX Cluster Resource Governor & Dynamic Admission Controller
Regulates CPU core allocations, memory budgets, and GPU leases across multi-tenant execution pools.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class TenantResourceBudget(BaseModel):
    tenant_id: str
    max_cpu_cores: float = 64.0
    allocated_cpu_cores: float = 0.0
    max_memory_gb: float = 256.0
    allocated_memory_gb: float = 0.0
    priority_level: int = 5  # 1 (Highest) to 10 (Lowest)


class ClusterResourceGovernor:
    """Controls cluster resource quotas and task admissions."""

    def __init__(self):
        self.budgets: Dict[str, TenantResourceBudget] = {}

    def register_tenant(self, budget: TenantResourceBudget) -> None:
        self.budgets[budget.tenant_id] = budget

    def request_allocation(self, tenant_id: str, cpus: float, memory_gb: float) -> bool:
        if tenant_id not in self.budgets:
            self.budgets[tenant_id] = TenantResourceBudget(tenant_id=tenant_id)

        b = self.budgets[tenant_id]
        if (b.allocated_cpu_cores + cpus <= b.max_cpu_cores) and (b.allocated_memory_gb + memory_gb <= b.max_memory_gb):
            b.allocated_cpu_cores += cpus
            b.allocated_memory_gb += memory_gb
            return True
        return False

    def release_allocation(self, tenant_id: str, cpus: float, memory_gb: float) -> None:
        if tenant_id in self.budgets:
            b = self.budgets[tenant_id]
            b.allocated_cpu_cores = max(0.0, b.allocated_cpu_cores - cpus)
            b.allocated_memory_gb = max(0.0, b.allocated_memory_gb - memory_gb)
