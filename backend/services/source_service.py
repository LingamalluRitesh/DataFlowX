"""
DataFlowX Data Source & Connector Service
Manages data source registration, credential encryption/decryption, connection health checks, and schema discovery.
"""

from datetime import datetime, timezone
import time
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.encryption import vault
from backend.core.exceptions import NotFoundError
from backend.core.logging import get_logger
from backend.database.models import ConnectionHealthLog, DataSource, SourceCredential, SourceSchemaSnapshot
from backend.schemas.common import PaginationParams
from backend.schemas.source import (
    ConnectionTestRequest,
    ConnectionTestResponse,
    DataSourceCreate,
    DataSourceUpdate,
    SchemaDiscoveryResponse,
)
from connectors.registry import ConnectorRegistry

logger = get_logger(__name__)


class SourceService:
    """Data source catalog and connectivity operations."""

    @staticmethod
    async def list_sources(session: AsyncSession, workspace_id: Optional[str], params: PaginationParams) -> Tuple[List[DataSource], int]:
        query = select(DataSource).where(DataSource.is_deleted == False)
        if workspace_id:
            query = query.where(DataSource.workspace_id == workspace_id)
        if params.search:
            s = f"%{params.search}%"
            query = query.where((DataSource.name.ilike(s)) | (DataSource.connector_type.ilike(s)))

        total_stmt = select(func.count()).select_from(query.subquery())
        total = (await session.execute(total_stmt)).scalar() or 0

        query = query.order_by(DataSource.created_at.desc()).offset((params.page - 1) * params.page_size).limit(params.page_size)
        items = (await session.execute(query)).scalars().all()
        return list(items), total

    @staticmethod
    async def get_source(session: AsyncSession, source_id: str) -> DataSource:
        src = (await session.execute(select(DataSource).where(DataSource.id == source_id, DataSource.is_deleted == False))).scalar_one_or_none()
        if not src:
            raise NotFoundError("DataSource", source_id)
        return src

    @staticmethod
    async def create_source(session: AsyncSession, workspace_id: Optional[str], payload: DataSourceCreate) -> DataSource:
        slug = payload.slug or payload.name.lower().replace(" ", "-")
        source = DataSource(
            workspace_id=workspace_id,
            name=payload.name,
            slug=slug,
            connector_type=payload.connector_type,
            description=payload.description,
            config=payload.config or {},
            is_active=payload.is_active,
            status="active"
        )
        session.add(source)
        await session.flush()

        if payload.credentials:
            encrypted = vault.encrypt_dict(payload.credentials)
            cred = SourceCredential(
                source_id=source.id,
                auth_type=payload.auth_type,
                encrypted_payload=encrypted,
                key_version=1
            )
            session.add(cred)

        await session.commit()
        await session.refresh(source)
        return source

    @staticmethod
    async def update_source(session: AsyncSession, source_id: str, payload: DataSourceUpdate) -> DataSource:
        source = await SourceService.get_source(session, source_id)
        if payload.name is not None:
            source.name = payload.name
        if payload.description is not None:
            source.description = payload.description
        if payload.config is not None:
            source.config = payload.config
        if payload.is_active is not None:
            source.is_active = payload.is_active

        if payload.credentials:
            cred = (await session.execute(select(SourceCredential).where(SourceCredential.source_id == source_id))).scalar_one_or_none()
            encrypted = vault.encrypt_dict(payload.credentials)
            if cred:
                cred.encrypted_payload = encrypted
            else:
                cred = SourceCredential(source_id=source_id, encrypted_payload=encrypted)
                session.add(cred)

        await session.commit()
        await session.refresh(source)
        return source

    @staticmethod
    async def delete_source(session: AsyncSession, source_id: str) -> None:
        source = await SourceService.get_source(session, source_id)
        source.soft_delete()
        await session.commit()

    @staticmethod
    async def test_connection(session: AsyncSession, source_id: str) -> ConnectionTestResponse:
        source = await SourceService.get_source(session, source_id)
        cred = (await session.execute(select(SourceCredential).where(SourceCredential.source_id == source_id))).scalar_one_or_none()
        credentials_dict = vault.decrypt_dict(cred.encrypted_payload) if cred else {}

        connector = ConnectorRegistry.create(source.connector_type, source.config, credentials_dict)
        test_res = connector.test_connection()

        # Log health check
        health_log = ConnectionHealthLog(
            source_id=source.id,
            status=test_res.status,
            latency_ms=test_res.latency_ms,
            error_message=test_res.message if not test_res.success else None,
            checked_at=datetime.now(timezone.utc)
        )
        session.add(health_log)
        source.last_health_check_at = datetime.now(timezone.utc)
        source.health_status = test_res.status
        await session.commit()

        return ConnectionTestResponse(
            success=test_res.success,
            status=test_res.status,
            latency_ms=test_res.latency_ms,
            message=test_res.message,
            details=test_res.details
        )

    @staticmethod
    async def discover_schema(session: AsyncSession, source_id: str) -> SchemaDiscoveryResponse:
        source = await SourceService.get_source(session, source_id)
        cred = (await session.execute(select(SourceCredential).where(SourceCredential.source_id == source_id))).scalar_one_or_none()
        credentials_dict = vault.decrypt_dict(cred.encrypted_payload) if cred else {}

        connector = ConnectorRegistry.create(source.connector_type, source.config, credentials_dict)
        disc_res = connector.discover_schema()

        # Store snapshot in DB
        snapshot = SourceSchemaSnapshot(
            source_id=source.id,
            raw_schema_json=disc_res.model_dump(mode="json"),
            table_count=len(disc_res.tables),
            column_count=sum(len(t.columns) for t in disc_res.tables),
            captured_at=datetime.now(timezone.utc)
        )
        session.add(snapshot)
        await session.commit()

        return SchemaDiscoveryResponse(
            source_id=source.id,
            connector_type=source.connector_type,
            tables=[
                {
                    "name": t.name,
                    "schema_name": t.schema_name,
                    "columns": [
                        {
                            "name": c.name,
                            "data_type": str(c.data_type.value if hasattr(c.data_type, "value") else c.data_type),
                            "is_nullable": c.is_nullable,
                            "is_primary_key": c.is_primary_key,
                            "sample_values": c.sample_values
                        }
                        for c in t.columns
                    ],
                    "estimated_rows": t.estimated_row_count
                }
                for t in disc_res.tables
            ],
            captured_at=datetime.now(timezone.utc)
        )
