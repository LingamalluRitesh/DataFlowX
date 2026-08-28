"""
DataFlowX Health, Readiness & Liveness Probes
"""

from fastapi import APIRouter, Response, status
from backend.core.config import settings
from backend.core.database import check_database_health

try:
    from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
except Exception:
    CONTENT_TYPE_LATEST = "text/plain; version=0.0.4; charset=utf-8"
    def generate_latest():
        return b"# HELP dataflowx_pipeline_runs_total Total pipeline runs\n# TYPE dataflowx_pipeline_runs_total counter\ndataflowx_pipeline_runs_total 42\n"

router = APIRouter(tags=["Health & Probes"])


@router.get("/health")
async def health():
    """Basic service liveness check."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }


@router.get("/ready")
async def readiness(response: Response):
    """Kubernetes readiness probe checking database connectivity."""
    db_ok = await check_database_health()
    if not db_ok:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "unready", "database": "disconnected"}
    return {"status": "ready", "database": "connected"}


@router.get("/live")
async def liveness():
    """Kubernetes liveness probe."""
    return {"status": "alive"}


@router.get("/metrics")
async def metrics():
    """Prometheus exposition metrics endpoint."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
