"""
DataFlowX Exception Hierarchy
Defines domain-specific and operational exceptions across all platform layers.
"""

from typing import Any, Dict, Optional


class DataFlowXException(Exception):
    """Base exception for all DataFlowX platform errors."""

    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_SERVER_ERROR",
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}


class AuthenticationError(DataFlowXException):
    """Raised when authentication fails or token is invalid."""

    def __init__(self, message: str = "Invalid credentials or token", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="AUTHENTICATION_FAILED", status_code=401, details=details)


class PermissionDeniedError(DataFlowXException):
    """Raised when user lacks required RBAC permissions."""

    def __init__(self, message: str = "Permission denied for this resource", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="PERMISSION_DENIED", status_code=403, details=details)


class NotFoundError(DataFlowXException):
    """Raised when a requested resource is missing."""

    def __init__(self, resource: str, resource_id: Any):
        message = f"{resource} with identifier '{resource_id}' was not found"
        super().__init__(message, code="RESOURCE_NOT_FOUND", status_code=404, details={"resource": resource, "id": str(resource_id)})


class ConflictError(DataFlowXException):
    """Raised when a resource state conflict occurs (e.g. duplicate key)."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="RESOURCE_CONFLICT", status_code=409, details=details)


class ValidationError(DataFlowXException):
    """Raised when payload or schema validation fails."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, code="VALIDATION_FAILED", status_code=422, details=details)


class ConnectorError(DataFlowXException):
    """Raised when data source connection, authentication, or extraction fails."""

    def __init__(self, connector_type: str, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            f"Connector [{connector_type}] error: {message}",
            code="CONNECTOR_ERROR",
            status_code=502,
            details=details or {"connector_type": connector_type}
        )


class DAGCycleError(DataFlowXException):
    """Raised when circular dependency is detected in pipeline DAG."""

    def __init__(self, message: str = "Circular dependency detected in pipeline graph", cycle_nodes: Optional[list] = None):
        super().__init__(
            message,
            code="DAG_CYCLE_DETECTED",
            status_code=400,
            details={"cycle_nodes": cycle_nodes or []}
        )


class DAGValidationError(DataFlowXException):
    """Raised when DAG topology or node connections are invalid."""

    def __init__(self, message: str, errors: Optional[list] = None):
        super().__init__(
            message,
            code="DAG_VALIDATION_ERROR",
            status_code=400,
            details={"validation_errors": errors or []}
        )


class ExecutionTimeoutError(DataFlowXException):
    """Raised when a pipeline or task execution exceeds timeout threshold."""

    def __init__(self, task_id: str, timeout_seconds: int):
        message = f"Task '{task_id}' exceeded execution timeout of {timeout_seconds}s"
        super().__init__(message, code="EXECUTION_TIMEOUT", status_code=504, details={"task_id": task_id, "timeout": timeout_seconds})


class QualityRuleFailedError(DataFlowXException):
    """Raised when critical data quality threshold fails."""

    def __init__(self, rule_name: str, score: float, threshold: float, failed_records: int):
        message = f"Quality rule '{rule_name}' failed with score {score:.2f}% (Threshold: {threshold:.2f}%)"
        super().__init__(
            message,
            code="DATA_QUALITY_FAILED",
            status_code=400,
            details={"rule_name": rule_name, "score": score, "threshold": threshold, "failed_records": failed_records}
        )


class ConcurrencyLockError(DataFlowXException):
    """Raised when a distributed lock cannot be acquired."""

    def __init__(self, lock_key: str):
        message = f"Could not acquire distributed lock for resource: {lock_key}"
        super().__init__(message, code="LOCK_ACQUISITION_FAILED", status_code=423, details={"lock_key": lock_key})


class StorageError(DataFlowXException):
    """Raised when file or object storage operations fail."""

    def __init__(self, message: str, path: Optional[str] = None):
        super().__init__(message, code="STORAGE_ERROR", status_code=500, details={"path": path})


class RateLimitExceededError(DataFlowXException):
    """Raised when an API rate limit is exceeded."""

    def __init__(self, retry_after: int = 60):
        super().__init__(
            f"Rate limit exceeded. Try again in {retry_after} seconds.",
            code="RATE_LIMIT_EXCEEDED",
            status_code=429,
            details={"retry_after": retry_after}
        )
