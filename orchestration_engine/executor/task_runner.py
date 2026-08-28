"""
DataFlowX Task Node Runner
Executes individual DAG nodes, handles data transformations, validations, quality checks, and telemetry capture.
"""

from datetime import datetime, timezone
import time
import traceback
from typing import Any, Dict, List, Optional, Tuple
import pandas as pd
from pydantic import BaseModel, Field
from backend.core.exceptions import DataFlowXException
from backend.core.logging import get_logger
from connectors.registry import ConnectorRegistry
from data_engine.medallion import MedallionManager
from data_engine.profiling import DataProfiler
from data_engine.quality import QualitySuiteEvaluator
from data_engine.transformation import (
    CustomPythonTransformer,
    CustomSQLTransformer,
    PipelineTransformer,
)
from data_engine.warehouse import WarehouseLoader
from orchestration_engine.dag.models import DAGNode, NodeType
from storage import ParquetManager, storage_engine

logger = get_logger(__name__)


class TaskExecutionResult(BaseModel):
    node_id: str
    name: str
    status: str  # SUCCESS, FAILED, SKIPPED
    start_time: datetime
    end_time: datetime
    duration_seconds: float
    records_in: int = 0
    records_out: int = 0
    bytes_processed: int = 0
    output_data: Optional[List[Dict[str, Any]]] = None  # Passed down to dependent tasks or parquet storage
    output_storage_uri: Optional[str] = None
    quality_score: Optional[float] = None
    error_message: Optional[str] = None
    error_traceback: Optional[str] = None
    logs: List[Dict[str, Any]] = Field(default_factory=list)


class TaskRunner:
    """Executes a single DAG node within an execution context."""

    def __init__(self, node: DAGNode, execution_id: str, pipeline_id: str):
        self.node = node
        self.execution_id = execution_id
        self.pipeline_id = pipeline_id
        self.logs: List[Dict[str, Any]] = []

    def _log(self, level: str, message: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        entry = {
            "level": level,
            "message": message,
            "metadata": metadata or {},
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.logs.append(entry)
        logger.info(f"[{self.execution_id[:8]}] [{self.node.id}] {message}")

    def execute(
        self,
        upstream_inputs: Dict[str, Any],
        context_globals: Optional[Dict[str, Any]] = None
    ) -> TaskExecutionResult:
        start_time = datetime.now(timezone.utc)
        t0 = time.time()
        self._log("INFO", f"Starting execution of node '{self.node.name}' (type={self.node.type})")

        ntype = self.node.type.lower()
        cfg = self.node.config or {}

        # Resolve primary input DataFrame from upstream outputs
        input_records: List[Dict[str, Any]] = []
        for parent_id, parent_output in upstream_inputs.items():
            if isinstance(parent_output, list) and parent_output:
                input_records = parent_output
                break
            elif isinstance(parent_output, dict) and "data" in parent_output:
                input_records = parent_output["data"]
                break

        records_in = len(input_records)
        df_in = pd.DataFrame(input_records) if input_records else pd.DataFrame()
        df_out = df_in.copy()
        output_storage_uri = None
        quality_score = None

        try:
            # 1. EXTRACT / SOURCE NODE
            if ntype in (NodeType.SOURCE.value, NodeType.EXTRACT.value):
                connector_type = cfg.get("connector_type", "csv")
                target = cfg.get("target") or cfg.get("file_path") or cfg.get("endpoint") or "default"
                connector_config = cfg.get("connector_config") or cfg
                credentials = cfg.get("credentials", {})

                self._log("INFO", f"Extracting data using connector '{connector_type}' from '{target}'")
                connector = ConnectorRegistry.create(connector_type, connector_config, credentials)
                connector.connect()

                # Extract preview or initial batch
                records = list(connector.preview_data(target, limit=int(cfg.get("limit", 10000))))
                connector.disconnect()

                df_out = pd.DataFrame(records)
                self._log("INFO", f"Extracted {len(df_out)} raw records from source")

                # Store raw in Bronze layer
                bronze_path = MedallionManager.store_bronze(
                    records=df_out.where(pd.notnull(df_out), None).to_dict(orient="records"),
                    dataset_name=self.node.name.replace(" ", "_").lower(),
                    execution_id=self.execution_id
                )
                output_storage_uri = bronze_path

            # 2. TRANSFORM / FILTER / DEDUPLICATE / AGGREGATE
            elif ntype in (
                NodeType.TRANSFORM.value,
                NodeType.FILTER.value,
                NodeType.DEDUPLICATE.value,
                NodeType.AGGREGATE.value,
                NodeType.SORT.value
            ):
                steps = cfg.get("steps", [])
                if not steps and "condition" in cfg:
                    steps = [{"type": "filter", "config": {"condition": cfg["condition"]}}]
                elif not steps and ntype == NodeType.DEDUPLICATE.value:
                    steps = [{"type": "deduplicate", "config": cfg}]
                elif not steps and ntype == NodeType.AGGREGATE.value:
                    steps = [{"type": "aggregate", "config": cfg}]

                transformer = PipelineTransformer(steps)
                df_out = transformer.transform(df_in)
                self._log("INFO", f"Transformation complete: {len(df_in)} -> {len(df_out)} records")

            # 3. SQL TRANSFORMATION NODE
            elif ntype == NodeType.SQL_JOB.value:
                query = cfg.get("query", "SELECT * FROM input_data")
                self._log("INFO", f"Executing SQL Transformation:\n{query}")
                sql_transformer = CustomSQLTransformer(query)
                df_out = sql_transformer.execute(df_in)
                self._log("INFO", f"SQL Transformation yielded {len(df_out)} rows")

            # 4. CUSTOM PYTHON SCRIPT NODE
            elif ntype == NodeType.PYTHON_JOB.value:
                script = cfg.get("script", "df = df")
                self._log("INFO", "Executing safe custom Python transformation")
                py_transformer = CustomPythonTransformer(script, timeout_seconds=cfg.get("timeout_seconds", 30))
                df_out = py_transformer.execute(df_in, context_params=context_globals)
                self._log("INFO", f"Python script finished: {len(df_out)} records")

            # 5. DATA QUALITY / VALIDATE NODE
            elif ntype in (NodeType.QUALITY.value, NodeType.VALIDATE.value):
                rules_cfg = cfg.get("rules", [])
                action = cfg.get("failure_action", "FAIL_PIPELINE")
                self._log("INFO", f"Evaluating {len(rules_cfg)} quality rules (failure_action={action})")

                evaluator = QualitySuiteEvaluator.from_check_configs(rules_cfg)
                summary, df_out = evaluator.evaluate(
                    df_in,
                    dataset_id=self.node.name,
                    execution_id=self.execution_id,
                    failure_action=action
                )
                quality_score = summary.overall_quality_score
                self._log("INFO", f"Data Quality evaluation completed with score {quality_score}% (Passed: {summary.is_suite_passed})")

                # Store validated clean data into Silver layer
                silver_path = MedallionManager.store_silver(
                    records=df_out.where(pd.notnull(df_out), None).to_dict(orient="records"),
                    dataset_name=self.node.name.replace(" ", "_").lower(),
                    execution_id=self.execution_id
                )
                output_storage_uri = silver_path

            # 6. WAREHOUSE LOAD NODE
            elif ntype == NodeType.WAREHOUSE_LOAD.value:
                tbl_name = cfg.get("table_name", f"analytics_{self.pipeline_id[:8]}")
                mode = cfg.get("mode", "upsert")
                pks = cfg.get("primary_keys", ["id"])
                self._log("INFO", f"Loading {len(df_in)} records into Warehouse table '{tbl_name}' ({mode})")

                # Store in Gold Lake
                gold_path = MedallionManager.store_gold(
                    records=df_in.where(pd.notnull(df_in), None).to_dict(orient="records"),
                    dataset_name=tbl_name,
                    execution_id=self.execution_id
                )
                output_storage_uri = gold_path

                # Load into Warehouse
                loader = WarehouseLoader()
                loader.load_gold_to_warehouse(
                    records=df_in.where(pd.notnull(df_in), None).to_dict(orient="records"),
                    table_name=tbl_name,
                    mode=mode,
                    primary_keys=pks
                )
                df_out = df_in
                self._log("INFO", f"Warehouse load complete: table '{tbl_name}' updated")

            # 7. DELAY NODE
            elif ntype == NodeType.DELAY.value:
                sec = int(cfg.get("seconds", 1))
                self._log("INFO", f"Pausing for {sec} seconds...")
                time.sleep(sec)
                df_out = df_in

            # 8. NOTIFICATION NODE
            elif ntype == NodeType.NOTIFICATION.value:
                channel = cfg.get("channel", "in_app")
                msg = cfg.get("message", "Pipeline step executed")
                self._log("INFO", f"Emitted notification via {channel}: {msg}")
                df_out = df_in

            # 9. CONDITIONAL BRANCH NODE
            elif ntype == NodeType.CONDITIONAL_BRANCH.value:
                condition = cfg.get("condition", "True")
                # Evaluate condition
                import sqlite3
                con = sqlite3.connect(":memory:")
                df_in.to_sql("input_data", con, index=False)
                res = con.execute(f"SELECT ({condition}) AS flag FROM input_data LIMIT 1").fetchone()
                branch_flag = bool(res[0]) if res else True
                con.close()
                self._log("INFO", f"Branch condition '{condition}' evaluated to: {branch_flag}")
                df_out = df_in

            end_time = datetime.now(timezone.utc)
            duration = time.time() - t0
            output_records = df_out.where(pd.notnull(df_out), None).to_dict(orient="records") if not df_out.empty else []

            return TaskExecutionResult(
                node_id=self.node.id,
                name=self.node.name,
                status="SUCCESS",
                start_time=start_time,
                end_time=end_time,
                duration_seconds=round(duration, 2),
                records_in=records_in,
                records_out=len(output_records),
                bytes_processed=int(df_out.memory_usage(deep=True).sum()) if not df_out.empty else 0,
                output_data=output_records,
                output_storage_uri=output_storage_uri,
                quality_score=quality_score,
                logs=self.logs
            )

        except Exception as exc:
            end_time = datetime.now(timezone.utc)
            duration = time.time() - t0
            tb = traceback.format_exc()
            self._log("ERROR", f"Task execution failed: {exc}", {"traceback": tb})

            return TaskExecutionResult(
                node_id=self.node.id,
                name=self.node.name,
                status="FAILED",
                start_time=start_time,
                end_time=end_time,
                duration_seconds=round(duration, 2),
                records_in=records_in,
                records_out=0,
                error_message=str(exc),
                error_traceback=tb,
                logs=self.logs
            )
