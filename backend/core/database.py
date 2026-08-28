"""
DataFlowX Database Configuration
Provides SQLAlchemy 2.0 Async and Sync Engines, Session Factories,
Declarative Base, and transaction helper utilities.
"""

from collections.abc import AsyncGenerator, Generator
from contextlib import asynccontextmanager, contextmanager
import logging
from typing import Any
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from backend.core.config import settings

logger = logging.getLogger(__name__)

from sqlalchemy import JSON

# Base Declarative Class
class Base(DeclarativeBase):
    pass

PortableJSON = JSON


# Async Engine Configuration (FastAPI Request Pipeline)
engine_kwargs: dict[str, Any] = {
    "echo": False,
    "future": True,
}

if not settings.DATABASE_URL.startswith("sqlite"):
    engine_kwargs.update({
        "pool_size": settings.DB_POOL_SIZE,
        "max_overflow": settings.DB_MAX_OVERFLOW,
        "pool_timeout": settings.DB_POOL_TIMEOUT,
        "pool_recycle": settings.DB_POOL_RECYCLE,
        "pool_pre_ping": True,
    })

engine = create_async_engine(
    settings.DATABASE_URL,
    **engine_kwargs
)

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Sync Engine Configuration (Workers, Schedulers, Migrations)
sync_engine_kwargs: dict[str, Any] = {
    "echo": False,
    "future": True,
}

if not settings.SYNC_DATABASE_URL.startswith("sqlite"):
    sync_engine_kwargs.update({
        "pool_size": 10,
        "max_overflow": 5,
        "pool_recycle": settings.DB_POOL_RECYCLE,
        "pool_pre_ping": True,
    })

sync_engine = create_engine(
    settings.SYNC_DATABASE_URL,
    **sync_engine_kwargs
)

sync_session_factory = sessionmaker(
    bind=sync_engine,
    class_=Session,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for injecting async database sessions into FastAPI routes."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def get_sync_db() -> Generator[Session, None, None]:
    """Context generator for worker and task executions."""
    session = sync_session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


@asynccontextmanager
async def async_transaction(session: AsyncSession):
    """Context manager for explicit transaction blocks."""
    if session.in_transaction():
        yield session
    else:
        async with session.begin():
            yield session


async def check_database_health() -> bool:
    """Execute a simple query to verify database connectivity."""
    try:
        async with async_session_factory() as session:
            result = await session.execute(text("SELECT 1"))
            return result.scalar() == 1
    except Exception as exc:
        logger.error(f"Database health check failed: {exc}")
        return False
