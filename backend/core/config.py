"""
DataFlowX Configuration Settings
Defines environment variables, runtime constants, and application configurations.
"""

import os
from typing import Any, List, Optional
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # General Application
    APP_NAME: str = "DataFlowX"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"  # development, staging, production, testing
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"

    # Server Bindings
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000

    # Cryptography & Security
    SECRET_KEY: str = "super-secret-system-key-change-this-in-production-dataflowx-2026"
    ENCRYPTION_MASTER_KEY: str = "k8A3VbE2QpY0zW1mN4xL7sJ5hF9cT6rU4dG1vK8wP2o="
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int = 24

    # CORS & Security Headers
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]
    ALLOWED_HOSTS: List[str] = ["*"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Any) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        return ["*"]

    # Database Configuration (PostgreSQL)
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "dataflowx"
    POSTGRES_PASSWORD: str = "dataflowx_secure_password"
    POSTGRES_DB: str = "dataflowx_metadata"
    DATABASE_URL: Optional[str] = None
    SYNC_DATABASE_URL: Optional[str] = None

    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_async_db_url(cls, v: Optional[str], info: Any) -> str:
        if v:
            return v
        values = info.data
        user = values.get("POSTGRES_USER", "dataflowx")
        pwd = values.get("POSTGRES_PASSWORD", "dataflowx_secure_password")
        server = values.get("POSTGRES_SERVER", "localhost")
        port = values.get("POSTGRES_PORT", 5432)
        db = values.get("POSTGRES_DB", "dataflowx_metadata")
        # For testing / local fallback SQLite can be enabled if requested, else asyncpg
        return f"sqlite+aiosqlite:///./dataflowx.db" if values.get("ENVIRONMENT") == "testing_sqlite" else f"postgresql+asyncpg://{user}:{pwd}@{server}:{port}/{db}"

    @field_validator("SYNC_DATABASE_URL", mode="before")
    @classmethod
    def assemble_sync_db_url(cls, v: Optional[str], info: Any) -> str:
        if v:
            return v
        values = info.data
        user = values.get("POSTGRES_USER", "dataflowx")
        pwd = values.get("POSTGRES_PASSWORD", "dataflowx_secure_password")
        server = values.get("POSTGRES_SERVER", "localhost")
        port = values.get("POSTGRES_PORT", 5432)
        db = values.get("POSTGRES_DB", "dataflowx_metadata")
        return f"sqlite:///./dataflowx.db" if values.get("ENVIRONMENT") == "testing_sqlite" else f"postgresql+psycopg2://{user}:{pwd}@{server}:{port}/{db}"

    # Redis Configuration
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0
    REDIS_URL: Optional[str] = None

    @field_validator("REDIS_URL", mode="before")
    @classmethod
    def assemble_redis_url(cls, v: Optional[str], info: Any) -> str:
        if v:
            return v
        values = info.data
        host = values.get("REDIS_HOST", "localhost")
        port = values.get("REDIS_PORT", 6379)
        pwd = values.get("REDIS_PASSWORD")
        db = values.get("REDIS_DB", 0)
        auth = f":{pwd}@" if pwd else ""
        return f"redis://{auth}{host}:{port}/{db}"

    # Celery Distributed Task Queue
    CELERY_BROKER_URL: Optional[str] = None
    CELERY_RESULT_BACKEND: Optional[str] = None
    CELERY_TASK_DEFAULT_QUEUE: str = "default"
    CELERY_TASK_HIGH_QUEUE: str = "high_priority"
    CELERY_TASK_LOW_QUEUE: str = "low_priority"

    @field_validator("CELERY_BROKER_URL", mode="before")
    @classmethod
    def assemble_celery_broker(cls, v: Optional[str], info: Any) -> str:
        if v:
            return v
        redis_url = info.data.get("REDIS_URL") or "redis://localhost:6379/1"
        return redis_url

    # Object Storage & Medallion Data Lake
    STORAGE_TYPE: str = "local"  # 'local', 's3', 'minio'
    LOCAL_STORAGE_BASE_PATH: str = "./storage"
    S3_ENDPOINT_URL: Optional[str] = "http://localhost:9000"
    S3_ACCESS_KEY_ID: str = "minioadmin"
    S3_SECRET_ACCESS_KEY: str = "minioadmin"
    S3_BUCKET_NAME: str = "dataflowx-lake"
    S3_REGION: str = "us-east-1"
    S3_SECURE: bool = False

    # Analytical Warehouse
    WAREHOUSE_TYPE: str = "duckdb"  # 'duckdb', 'postgres', 'clickhouse'
    WAREHOUSE_DATABASE_URL: Optional[str] = None
    WAREHOUSE_DUCKDB_PATH: str = "./storage/warehouse/analytics.duckdb"

    # Metrics & Observability
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 120
    AUTH_RATE_LIMIT_PER_MINUTE: int = 15

    # Notification & Alerting Channels
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM_EMAIL: str = "alerts@dataflowx.io"
    SLACK_WEBHOOK_URL: Optional[str] = None
    DEFAULT_ALERT_WEBHOOK: Optional[str] = None

    # Initial Bootstrapping
    INITIAL_ADMIN_EMAIL: str = "admin@dataflowx.io"
    INITIAL_ADMIN_PASSWORD: str = "Admin@DataFlowX2026!"
    INITIAL_ADMIN_FULL_NAME: str = "System Super Administrator"
    INITIAL_ORG_NAME: str = "Global Enterprise Corp"
    INITIAL_WORKSPACE_NAME: str = "Production Analytics"


settings = Settings()
