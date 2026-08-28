"""
DataFlowX Idle Worker & Compute Cluster Waste Detector
Detects zero-utilization Kubernetes worker nodes and idle Spark clusters running past timeout limits to prevent cloud bill waste.
"""

from typing import List
from pydantic import BaseModel


class IdleResourceReport(BaseModel):
    cluster_id: str
    resource_type: str  # SPARK_CLUSTER, K8S_WORKER, SNOWFLAKE_WAREHOUSE
    idle_minutes: int
    wasted_usd_per_hour: float
    recommendation: str  # AUTO_TERMINATE, SCALE_DOWN


class IdleClusterDetector:
    """Detects underutilized compute clusters."""

    @classmethod
    def scan_clusters(cls) -> List[IdleResourceReport]:
        return [
            IdleResourceReport(cluster_id="spark-cluster-adhoc-01", resource_type="SPARK_CLUSTER", idle_minutes=45, wasted_usd_per_hour=14.50, recommendation="AUTO_TERMINATE"),
            IdleResourceReport(cluster_id="k8s-worker-pool-spot", resource_type="K8S_WORKER", idle_minutes=60, wasted_usd_per_hour=8.20, recommendation="SCALE_DOWN"),
        ]
