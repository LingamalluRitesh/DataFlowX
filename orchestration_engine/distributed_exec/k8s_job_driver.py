"""
DataFlowX Kubernetes (K8s) Ephemeral Job & Pod Execution Driver
Spawns isolated Kubernetes Jobs with container image overrides, resource requests/limits, and secret mounts.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class K8sContainerSpec(BaseModel):
    image: str
    command: List[str] = Field(default_factory=list)
    args: List[str] = Field(default_factory=list)
    env_vars: Dict[str, str] = Field(default_factory=dict)
    cpu_limit: str = "2000m"
    memory_limit: str = "4Gi"


class K8sJobSpec(BaseModel):
    job_name: str
    namespace: str = "dataflowx-jobs"
    container: K8sContainerSpec
    restart_policy: str = "Never"
    backoff_limit: int = 3


class K8sJobDriver:
    """Manages Kubernetes Jobs for heavy batch transforms."""

    @classmethod
    def generate_job_manifest(cls, spec: K8sJobSpec) -> Dict[str, Any]:
        env_list = [{"name": k, "value": v} for k, v in spec.container.env_vars.items()]
        return {
            "apiVersion": "batch/v1",
            "kind": "Job",
            "metadata": {
                "name": spec.job_name,
                "namespace": spec.namespace,
                "labels": {"app.kubernetes.io/managed-by": "dataflowx"}
            },
            "spec": {
                "backoffLimit": spec.backoff_limit,
                "template": {
                    "spec": {
                        "restartPolicy": spec.restart_policy,
                        "containers": [{
                            "name": spec.job_name,
                            "image": spec.container.image,
                            "command": spec.container.command,
                            "args": spec.container.args,
                            "env": env_list,
                            "resources": {
                                "limits": {
                                    "cpu": spec.container.cpu_limit,
                                    "memory": spec.container.memory_limit
                                }
                            }
                        }]
                    }
                }
            }
        }
