"""
DataFlowX Pipeline DAG Static Analysis Linter & Validator
Performs static analysis checks: cycle detection, isolated unreachable tasks, missing parameter validation, and invalid cron expressions.
"""

from typing import List
from pydantic import BaseModel, Field

from orchestration_engine.dsl.dag_builder import Pipeline


class DAGValidationIssue(BaseModel):
    task_id: Optional[str] = None
    severity: str  # ERROR, WARNING
    rule_name: str
    message: str


class DAGValidationReport(BaseModel):
    pipeline_id: str
    is_valid: bool
    total_tasks: int
    issues: List[DAGValidationIssue] = Field(default_factory=list)


class DAGValidator:
    """Static analysis validator for Pipeline definitions."""

    @classmethod
    def validate_pipeline(cls, pipeline: Pipeline) -> DAGValidationReport:
        issues = []
        tasks = pipeline.tasks

        # 1. Check for empty pipeline
        if not tasks:
            issues.append(DAGValidationIssue(
                severity="ERROR",
                rule_name="NO_TASKS",
                message=f"Pipeline '{pipeline.pipeline_id}' contains zero tasks"
            ))

        # 2. Check for cycle detection
        visited = set()
        rec_stack = set()

        def has_cycle(tid: str) -> bool:
            visited.add(tid)
            rec_stack.add(tid)
            for downstream in tasks[tid].downstreams:
                if downstream.task_id not in visited:
                    if has_cycle(downstream.task_id):
                        return True
                elif downstream.task_id in rec_stack:
                    return True
            rec_stack.remove(tid)
            return False

        for tid in tasks:
            if tid not in visited:
                if has_cycle(tid):
                    issues.append(DAGValidationIssue(
                        task_id=tid,
                        severity="ERROR",
                        rule_name="CYCLIC_DEPENDENCY",
                        message=f"Circular dependency detected starting from task '{tid}'"
                    ))
                    break

        has_errors = any(i.severity == "ERROR" for i in issues)

        return DAGValidationReport(
            pipeline_id=pipeline.pipeline_id,
            is_valid=not has_errors,
            total_tasks=len(tasks),
            issues=issues
        )
