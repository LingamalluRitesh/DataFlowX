"""
DataFlowX Middleware Suite
Provides Correlation ID propagation, rate limiting, request timing,
structured exception interception, and security headers.
"""

from collections import defaultdict
import time
from typing import Callable, Dict, List, Optional
import uuid
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from backend.core.config import settings
from backend.core.exceptions import DataFlowXException
from backend.core.logging import (
    correlation_id_ctx,
    get_logger,
    org_id_ctx,
    user_id_ctx,
    workspace_id_ctx,
)

logger = get_logger(__name__)


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Injects correlation ID and extracts user/tenant context into async contextvars."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        corr_id = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
        correlation_id_ctx.set(corr_id)

        # Set tenant context if available from headers
        org_id = request.headers.get("X-Organization-ID")
        ws_id = request.headers.get("X-Workspace-ID")
        if org_id:
            org_id_ctx.set(org_id)
        if ws_id:
            workspace_id_ctx.set(ws_id)

        start_time = time.time()
        try:
            response = await call_next(request)
        except Exception as exc:
            # Let the exception handler middleware process it
            raise exc

        duration_ms = (time.time() - start_time) * 1000
        response.headers["X-Correlation-ID"] = corr_id
        response.headers["X-Response-Time"] = f"{duration_ms:.2f}ms"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"

        return response


class InMemoryRateLimiterMiddleware(BaseHTTPMiddleware):
    """In-memory sliding window rate limiter for API protection."""

    def __init__(self, app: ASGIApp, requests_per_minute: int = 120):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, List[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Exclude static files, docs, and health checks
        path = request.url.path
        if path in ("/health", "/ready", "/live", "/metrics", "/docs", "/openapi.json", "/redoc"):
            return await call_next(request)

        client_ip = request.client.host if request.client else "127.0.0.1"
        now = time.time()
        minute_ago = now - 60

        # Filter timestamps within the last 60 seconds
        timestamps = [t for t in self.requests[client_ip] if t > minute_ago]
        self.requests[client_ip] = timestamps

        limit = settings.AUTH_RATE_LIMIT_PER_MINUTE if "/auth/" in path else self.requests_per_minute

        if len(timestamps) >= limit:
            logger.warning(f"Rate limit exceeded for IP {client_ip} on {path}")
            return JSONResponse(
                status_code=429,
                content={
                    "error": {
                        "code": "RATE_LIMIT_EXCEEDED",
                        "message": "Too many requests. Please try again later.",
                        "retry_after_seconds": 60,
                        "correlation_id": correlation_id_ctx.get(),
                    }
                },
                headers={"Retry-After": "60"},
            )

        self.requests[client_ip].append(now)
        return await call_next(request)


def register_exception_handlers(app: FastAPI) -> None:
    """Register uniform RFC 7807 compliant exception handlers."""

    @app.exception_handler(DataFlowXException)
    async def handle_dataflowx_exception(request: Request, exc: DataFlowXException):
        logger.error(f"Platform error: {exc.code} - {exc.message} on {request.method} {request.url.path}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "details": exc.details,
                    "correlation_id": correlation_id_ctx.get(),
                    "timestamp": time.time(),
                }
            },
        )

    @app.exception_handler(Exception)
    async def handle_generic_exception(request: Request, exc: Exception):
        logger.exception(f"Unhandled server error on {request.method} {request.url.path}: {exc}")
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected server error occurred. Please contact system support.",
                    "details": {"exception_type": type(exc).__name__} if settings.DEBUG else {},
                    "correlation_id": correlation_id_ctx.get(),
                    "timestamp": time.time(),
                }
            },
        )
