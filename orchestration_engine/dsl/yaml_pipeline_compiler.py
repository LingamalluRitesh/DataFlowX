"""
DataFlowX Declarative YAML Pipeline Compiler
Compiles declarative YAML workflow configuration files into executable Pipeline DAG instances.
"""

from typing import Any, Dict, List, Optional
import yaml
from orchestration_engine.dsl.dag_builder import Pipeline, TaskNode


class YAMLPipelineCompiler:
    """Compiles YAML text to Pipeline objects."""

    @classmethod
    def compile_yaml(cls, yaml_content: str) -> Pipeline:
        data = yaml.safe_load(yaml_content)
        if not data or "pipeline" not in data:
            raise ValueError("YAML must contain root 'pipeline' key")

        meta = data["pipeline"]
        pipe = Pipeline(
            pipeline_id=meta.get("id", "unnamed_pipeline"),
            schedule_cron=meta.get("schedule"),
            description=meta.get("description"),
            tags=meta.get("tags", [])
        )

        tasks_data = data.get("tasks", [])
        created_tasks: Dict[str, TaskNode] = {}

        # 1. Create task nodes
        for t_spec in tasks_data:
            tid = t_spec["id"]
            op_type = t_spec.get("type", "GenericOperator")
            params = t_spec.get("parameters", {})
            retries = t_spec.get("retries", 3)

            task = TaskNode(
                task_id=tid,
                operator_type=op_type,
                parameters=params,
                retries=retries
            )
            pipe.add_task(task)
            created_tasks[tid] = task

        # 2. Wire dependencies
        for t_spec in tasks_data:
            tid = t_spec["id"]
            depends_on = t_spec.get("depends_on", [])
            for upstream_id in depends_on:
                if upstream_id in created_tasks:
                    created_tasks[upstream_id] >> created_tasks[tid]

        return pipe
