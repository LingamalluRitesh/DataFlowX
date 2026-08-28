"""
DataFlowX DAG Pipeline Execution Engine
Orchestrates parallel and sequential execution of DAG layers, coordinates state transitions, retry policies, and telemetry.
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from backend.core.logging import get_logger
from orchestration_engine.dag.dag_parser import DAGParser
from orchestration_engine.dag.models import DAGDefinition
from orchestration_engine.executor.task_runner import TaskExecutionResult, TaskRunner
from orchestration_engine.retry.policy import RetryPolicy

logger = get_logger(__name__)


class PipelineExecutionSummary(BaseModel):
    execution_id: str
    pipeline_id: str
    status: str  # SUCCESS, FAILED, CANCELLED
    start_time: datetime
    end_time: datetime
    duration_seconds: float
    total_records_processed: int
    total_bytes_processed: int
    records_failed: int
    quality_score: Optional[float] = None
    tasks_count: int
    successful_tasks: int
    failed_tasks: int
    skipped_tasks: int
    task_results: Dict[str, TaskExecutionResult] = Field(default_factory=dict)
    error_summary: Optional[str] = None


class DAGExecutor:
    """Orchestrates end-to-end pipeline graph execution."""

    def __init__(
        self,
        dag_definition: DAGDefinition,
        pipeline_id: str,
        execution_id: str,
        max_workers: int = 4,
        retry_policy: Optional[RetryPolicy] = None
    ):
        self.dag = dag_definition
        self.pipeline_id = pipeline_id
        self.execution_id = execution_id
        self.max_workers = max_workers
        self.retry_policy = retry_policy or RetryPolicy(max_retries=2, base_delay_seconds=1.0)
        self.parser = DAGParser(self.dag)
        self.xcom_context: Dict[str, Any] = {}  # task_id -> output_data

    def run(self, runtime_parameters: Optional[Dict[str, Any]] = None) -> PipelineExecutionSummary:
        start_time = datetime.now(timezone.utc)
        t0 = time.time()
        logger.info(f"Initiating execution '{self.execution_id}' for pipeline '{self.pipeline_id}'")

        # 1. Validate DAG
        is_valid, errors, warnings = self.parser.validate_dag()
        if not is_valid:
            end_time = datetime.now(timezone.utc)
            err_msg = f"DAG validation failed: {'; '.join(errors)}"
            logger.error(err_msg)
            return PipelineExecutionSummary(
                execution_id=self.execution_id,
                pipeline_id=self.pipeline_id,
                status="FAILED",
                start_time=start_time,
                end_time=end_time,
                duration_seconds=round(time.time() - t0, 2),
                total_records_processed=0,
                total_bytes_processed=0,
                records_failed=0,
                tasks_count=len(self.dag.nodes),
                successful_tasks=0,
                failed_tasks=len(self.dag.nodes),
                skipped_tasks=0,
                error_summary=err_msg
            )

        # 2. Get execution layers
        layers = self.parser.get_execution_layers()
        task_results: Dict[str, TaskExecutionResult] = {}
        pipeline_failed = False
        first_error_msg = None

        globals_ctx = dict(self.dag.globals)
        if runtime_parameters:
            globals_ctx.update(runtime_parameters)

        # 3. Execute layer by layer
        for layer_idx, node_ids in enumerate(layers):
            if pipeline_failed:
                # Skip remaining tasks
                for nid in node_ids:
                    node = self.parser.nodes_by_id[nid]
                    now = datetime.now(timezone.utc)
                    task_results[nid] = TaskExecutionResult(
                        node_id=nid,
                        name=node.name,
                        status="SKIPPED",
                        start_time=now,
                        end_time=now,
                        duration_seconds=0.0,
                        error_message="Skipped due to upstream failure"
                    )
                continue

            logger.info(f"Executing DAG Layer {layer_idx + 1}/{len(layers)} with {len(node_ids)} concurrent tasks: {node_ids}")

            # Run nodes in current layer
            def _run_single_node(nid: str) -> TaskExecutionResult:
                node = self.parser.nodes_by_id[nid]
                upstreams = self.parser.get_upstream_dependencies(nid)

                # Gather upstream outputs
                inputs: Dict[str, Any] = {}
                for up_id in upstreams:
                    if up_id in self.xcom_context:
                        inputs[up_id] = self.xcom_context[up_id]

                runner = TaskRunner(node, self.execution_id, self.pipeline_id)

                # Execute with retry policy
                def _do_execute():
                    res = runner.execute(inputs, globals_ctx)
                    if res.status == "FAILED":
                        raise RuntimeError(res.error_message or "Task execution failed")
                    return res

                try:
                    return self.retry_policy.execute_with_retry(_do_execute)
                except Exception as exc:
                    now = datetime.now(timezone.utc)
                    return TaskExecutionResult(
                        node_id=nid,
                        name=node.name,
                        status="FAILED",
                        start_time=now,
                        end_time=now,
                        duration_seconds=0.0,
                        error_message=str(exc)
                    )

            if len(node_ids) == 1:
                res = _run_single_node(node_ids[0])
                task_results[node_ids[0]] = res
                if res.status == "SUCCESS":
                    self.xcom_context[node_ids[0]] = res.output_data
                else:
                    pipeline_failed = True
                    first_error_msg = res.error_message
            else:
                with ThreadPoolExecutor(max_workers=min(self.max_workers, len(node_ids))) as pool:
                    futures = {pool.submit(_run_single_node, nid): nid for nid in node_ids}
                    for fut in as_completed(futures):
                        nid = futures[fut]
                        res = fut.result()
                        task_results[nid] = res
                        if res.status == "SUCCESS":
                            self.xcom_context[nid] = res.output_data
                        else:
                            pipeline_failed = True
                            if not first_error_msg:
                                first_error_msg = res.error_message

        end_time = datetime.now(timezone.utc)
        duration = round(time.time() - t0, 2)

        # 4. Compute pipeline-level aggregates
        successful_cnt = sum(1 for r in task_results.values() if r.status == "SUCCESS")
        failed_cnt = sum(1 for r in task_results.values() if r.status == "FAILED")
        skipped_cnt = sum(1 for r in task_results.values() if r.status == "SKIPPED")
        total_recs = max([r.records_out for r in task_results.values()], default=0)
        total_bytes = sum(r.bytes_processed for r in task_results.values())

        quality_scores = [r.quality_score for r in task_results.values() if r.quality_score is not None]
        avg_quality = (sum(quality_scores) / len(quality_scores)) if quality_scores else None

        final_status = "SUCCESS" if (failed_cnt == 0 and not pipeline_failed) else "FAILED"
        logger.info(f"Pipeline execution '{self.execution_id}' finished with status {final_status} in {duration}s")

        return PipelineExecutionSummary(
            execution_id=self.execution_id,
            pipeline_id=self.pipeline_id,
            status=final_status,
            start_time=start_time,
            end_time=end_time,
            duration_seconds=duration,
            total_records_processed=total_recs,
            total_bytes_processed=total_bytes,
            records_failed=sum(r.records_in - r.records_out for r in task_results.values() if r.records_in > r.records_out),
            quality_score=avg_quality,
            tasks_count=len(self.dag.nodes),
            successful_tasks=successful_cnt,
            failed_tasks=failed_cnt,
            skipped_tasks=skipped_cnt,
            task_results=task_results,
            error_summary=first_error_msg
        )
