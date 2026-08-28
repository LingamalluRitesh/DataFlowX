"""
DataFlowX API v1 Router Aggregator
Combines all domain routers under /api/v1.
"""

from fastapi import APIRouter
from backend.api.v1.audit import router as audit_router
from backend.api.v1.auth import router as auth_router
from backend.api.v1.backfills import router as backfills_router
from backend.api.v1.catalog import router as catalog_router
from backend.api.v1.contracts import router as contracts_router
from backend.api.v1.datasets import router as datasets_router
from backend.api.v1.executions import router as executions_router
from backend.api.v1.health import router as health_router
from backend.api.v1.lineage import router as lineage_router
from backend.api.v1.monitoring import router as monitoring_router
from backend.api.v1.organizations import router as organizations_router
from backend.api.v1.pipelines import router as pipelines_router
from backend.api.v1.privacy import router as privacy_router
from backend.api.v1.quality import router as quality_router
from backend.api.v1.query import router as query_router
from backend.api.v1.sensors import router as sensors_router
from backend.api.v1.sources import router as sources_router
from backend.api.v1.streaming import router as streaming_router
from backend.api.v1.users import router as users_router

api_v1_router = APIRouter()

# Register domain routers
api_v1_router.include_router(auth_router)
api_v1_router.include_router(users_router)
api_v1_router.include_router(organizations_router)
api_v1_router.include_router(sources_router)
api_v1_router.include_router(datasets_router)
api_v1_router.include_router(pipelines_router)
api_v1_router.include_router(executions_router)
api_v1_router.include_router(quality_router)
api_v1_router.include_router(lineage_router)
api_v1_router.include_router(catalog_router)
api_v1_router.include_router(contracts_router)
api_v1_router.include_router(privacy_router)
api_v1_router.include_router(backfills_router)
api_v1_router.include_router(sensors_router)
api_v1_router.include_router(query_router)
api_v1_router.include_router(streaming_router)
api_v1_router.include_router(monitoring_router)
api_v1_router.include_router(audit_router)
api_v1_router.include_router(health_router)

__all__ = ["api_v1_router"]
