"""
DataFlowX Celery Distributed Task Queue Application
Configures broker, result backend, task routing, priority queues, and workers.
"""

import os
try:
    from celery import Celery
    from kombu import Exchange, Queue

    # Initialize Celery app
    celery_app = Celery(
        "dataflowx",
        broker=settings.CELERY_BROKER_URL,
        backend=settings.CELERY_RESULT_BACKEND,
    )

    # Configure exchanges and priority queues
    default_exchange = Exchange("dataflowx", type="direct")

    celery_app.conf.task_queues = (
        Queue(settings.CELERY_TASK_HIGH_QUEUE, default_exchange, routing_key="task.high", queue_arguments={"x-max-priority": 10}),
        Queue(settings.CELERY_TASK_DEFAULT_QUEUE, default_exchange, routing_key="task.default", queue_arguments={"x-max-priority": 5}),
        Queue(settings.CELERY_TASK_LOW_QUEUE, default_exchange, routing_key="task.low", queue_arguments={"x-max-priority": 1}),
    )

    celery_app.conf.task_default_queue = settings.CELERY_TASK_DEFAULT_QUEUE
    celery_app.conf.task_default_exchange = "dataflowx"
    celery_app.conf.task_default_routing_key = "task.default"

    celery_app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
        task_track_started=True,
        task_time_limit=7200,  # 2 hours
        worker_prefetch_multiplier=1,
        worker_concurrency=int(os.cpu_count() or 4),
    )

    def execute_pipeline_task(task_payload: dict) -> dict:
        from orchestration_engine.dag.models import DAGNode
        from orchestration_engine.executor.task_runner import TaskRunner

        node_data = task_payload.get("node")
        execution_id = task_payload.get("execution_id")
        pipeline_id = task_payload.get("pipeline_id")
        inputs = task_payload.get("inputs", {})
        globals_ctx = task_payload.get("globals", {})

        node = DAGNode(**node_data)
        runner = TaskRunner(node, execution_id, pipeline_id)
        result = runner.execute(inputs, globals_ctx)
        return result.model_dump(mode="json")

except Exception:
    celery_app = None

    def execute_pipeline_task(task_payload: dict) -> dict:
        from orchestration_engine.dag.models import DAGNode
        from orchestration_engine.executor.task_runner import TaskRunner

        node_data = task_payload.get("node")
        execution_id = task_payload.get("execution_id")
        pipeline_id = task_payload.get("pipeline_id")
        inputs = task_payload.get("inputs", {})
        globals_ctx = task_payload.get("globals", {})

        node = DAGNode(**node_data)
        runner = TaskRunner(node, execution_id, pipeline_id)
        result = runner.execute(inputs, globals_ctx)
        return result.model_dump(mode="json")



