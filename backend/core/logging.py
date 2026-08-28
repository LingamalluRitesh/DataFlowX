"""
DataFlowX Structured Logging System
Provides JSON structured logging, context propagation (correlation ID, execution ID, task ID),
sensitive data scrubbing, and console/file stream routing.
"""

from contextvars import ContextVar
from datetime import datetime, timezone
import json
import logging
import os
import re
import sys
from typing import Any, Dict, Optional

# Context variables for distributed request tracing
correlation_id_ctx: ContextVar[Optional[str]] = ContextVar("correlation_id", default=None)
user_id_ctx: ContextVar[Optional[str]] = ContextVar("user_id", default=None)
org_id_ctx: ContextVar[Optional[str]] = ContextVar("org_id", default=None)
workspace_id_ctx: ContextVar[Optional[str]] = ContextVar("workspace_id", default=None)
execution_id_ctx: ContextVar[Optional[str]] = ContextVar("execution_id", default=None)
task_id_ctx: ContextVar[Optional[str]] = ContextVar("task_id", default=None)

SENSITIVE_PATTERNS = [
    re.compile(r'(password["\']?\s*[:=]\s*["\'])([^"\']+)(["\'])', re.IGNORECASE),
    re.compile(r'(secret["\']?\s*[:=]\s*["\'])([^"\']+)(["\'])', re.IGNORECASE),
    re.compile(r'(token["\']?\s*[:=]\s*["\'])([^"\']+)(["\'])', re.IGNORECASE),
    re.compile(r'(api[_-]?key["\']?\s*[:=]\s*["\'])([^"\']+)(["\'])', re.IGNORECASE),
    re.compile(r'(authorization["\']?\s*[:=]\s*["\']bearer\s+)([^"\']+)(["\'])', re.IGNORECASE),
]


def mask_sensitive_strings(text: str) -> str:
    """Scrub sensitive credentials from log strings."""
    if not isinstance(text, str):
        return text
    masked = text
    for pattern in SENSITIVE_PATTERNS:
        masked = pattern.sub(r'\1********\3', masked)
    return masked


class JSONLogFormatter(logging.Formatter):
    """Formats log records as structured JSON with contextual tracking fields."""

    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": mask_sensitive_strings(record.getMessage()),
            "module": record.module,
            "func_name": record.funcName,
            "line_no": record.lineno,
            "process_id": os.getpid(),
        }

        # Inject context variables
        corr_id = correlation_id_ctx.get()
        if corr_id:
            log_data["correlation_id"] = corr_id

        usr_id = user_id_ctx.get()
        if usr_id:
            log_data["user_id"] = usr_id

        org_id = org_id_ctx.get()
        if org_id:
            log_data["org_id"] = org_id

        ws_id = workspace_id_ctx.get()
        if ws_id:
            log_data["workspace_id"] = ws_id

        exec_id = execution_id_ctx.get()
        if exec_id:
            log_data["execution_id"] = exec_id

        t_id = task_id_ctx.get()
        if t_id:
            log_data["task_id"] = t_id

        # Attach extra dictionary attributes if present
        if hasattr(record, "extra_data") and isinstance(record.extra_data, dict):
            log_data["data"] = record.extra_data

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


def setup_logging(level: str = "INFO", json_format: bool = True) -> None:
    """Configure root logger with structured JSON or human-readable format."""
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    console_handler = logging.StreamHandler(sys.stdout)
    if json_format:
        console_handler.setFormatter(JSONLogFormatter())
    else:
        plain_fmt = "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
        console_handler.setFormatter(logging.Formatter(plain_fmt))

    root_logger.addHandler(console_handler)

    # Silence overly verbose external libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("boto3").setLevel(logging.WARNING)
    logging.getLogger("botocore").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Obtain a logger instance with DataFlowX conventions."""
    return logging.getLogger(name)
