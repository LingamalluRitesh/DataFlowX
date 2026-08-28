"""
DataFlowX Standard Operator Library
Provides built-in operator wrapper classes: ExtractOperator, TransformOperator, QualityCheckOperator, LakehouseLoadOperator, SlackAlertOperator, SparkSubmitOperator, HTTPWebhookOperator.
"""

from typing import Any, Callable, Dict, List, Optional
from orchestration_engine.dsl.dag_builder import Pipeline, TaskNode


class BaseOperator(TaskNode):
    """Base class for all DSL operators."""

    def __init__(self, task_id: str, **kwargs: Any):
        super().__init__(task_id=task_id, operator_type=self.__class__.__name__, parameters=kwargs)
        if Pipeline._CURRENT_PIPELINE:
            Pipeline._CURRENT_PIPELINE.add_task(self)


class PostgresExtractOperator(BaseOperator):
    def __init__(self, task_id: str, query: str, connection_id: str, **kwargs: Any):
        super().__init__(task_id=task_id, query=query, connection_id=connection_id, **kwargs)


class S3LakehouseLoadOperator(BaseOperator):
    def __init__(self, task_id: str, target_bucket: str, layer: str = "BRONZE", format: str = "PARQUET", **kwargs: Any):
        super().__init__(task_id=task_id, target_bucket=target_bucket, layer=layer, format=format, **kwargs)


class QualityAssertionOperator(BaseOperator):
    def __init__(self, task_id: str, rules: List[str], threshold_pct: float = 99.0, **kwargs: Any):
        super().__init__(task_id=task_id, rules=rules, threshold_pct=threshold_pct, **kwargs)


class SnowflakeMergeOperator(BaseOperator):
    def __init__(self, task_id: str, target_table: str, join_keys: List[str], **kwargs: Any):
        super().__init__(task_id=task_id, target_table=target_table, join_keys=join_keys, **kwargs)


class SparkSubmitOperator(BaseOperator):
    def __init__(self, task_id: str, application_path: str, master: str = "k8s://...", **kwargs: Any):
        super().__init__(task_id=task_id, application_path=application_path, master=master, **kwargs)


class SlackNotificationOperator(BaseOperator):
    def __init__(self, task_id: str, channel: str, message: str, **kwargs: Any):
        super().__init__(task_id=task_id, channel=channel, message=message, **kwargs)


class PythonExecuteOperator(BaseOperator):
    def __init__(self, task_id: str, python_callable: Callable[..., Any], **kwargs: Any):
        super().__init__(task_id=task_id, python_callable=python_callable, **kwargs)
