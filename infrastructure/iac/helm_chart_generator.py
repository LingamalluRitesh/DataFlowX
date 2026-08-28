"""
DataFlowX Kubernetes Helm Chart Values Generator
Generates production Kubernetes Helm values.yaml for deploying autoscaled DataFlowX worker pods, Raft coordinators, and API gateways.
"""

class HelmChartValuesGenerator:
    """Generates Helm values."""

    @classmethod
    def generate_values_yaml(cls, replica_count: int = 4, memory_limit: str = "4Gi", cpu_limit: str = "2000m") -> str:
        yaml_str = f"""
# DataFlowX Production Helm Chart Values
replicaCount: {replica_count}

image:
  repository: dataflowx/orchestrator
  pullPolicy: IfNotPresent
  tag: "v2.0.0"

resources:
  limits:
    cpu: {cpu_limit}
    memory: {memory_limit}
  requests:
    cpu: "500m"
    memory: "1Gi"

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 16
  targetCPUUtilizationPercentage: 80
        """.strip()
        return yaml_str
