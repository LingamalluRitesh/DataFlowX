"""
DataFlowX FastAPI Master Application Entrypoint
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.v1 import api_v1_router
from backend.core.config import settings
from backend.core.database import Base, engine
from backend.core.logging import get_logger, setup_logging
from backend.core.middleware import (
    InMemoryRateLimiterMiddleware,
    RequestContextMiddleware,
    register_exception_handlers,
)

# Initialize structured logging
setup_logging(level="DEBUG" if settings.DEBUG else "INFO")
logger = get_logger("dataflowx.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    logger.info(f"Initializing {settings.APP_NAME} v{settings.APP_VERSION} ({settings.ENVIRONMENT})...")

    # In development or testing with sqlite/postgres create tables if needed
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database metadata schema synchronized.")

    yield

    logger.info("Shutting down DataFlowX backend services...")
    await engine.dispose()


app = FastAPI(
    title="DataFlowX API",
    description="Intelligent Enterprise Data Pipeline & Orchestration Platform REST API",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# 1. Register Global Exception Handlers
register_exception_handlers(app)

# 2. CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Rate Limiting Middleware
app.add_middleware(InMemoryRateLimiterMiddleware, requests_per_minute=settings.RATE_LIMIT_PER_MINUTE)

# 4. Request Context & Correlation ID Middleware
app.add_middleware(RequestContextMiddleware)

# 5. Include API Routers
app.include_router(api_v1_router, prefix=settings.API_V1_STR)
# Also include health probes at root level for Kubernetes
from backend.api.v1.health import router as root_health_router
app.include_router(root_health_router)


@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "operational",
        "docs": "/docs",
        "api_v1": settings.API_V1_STR,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=settings.DEBUG,
    )
