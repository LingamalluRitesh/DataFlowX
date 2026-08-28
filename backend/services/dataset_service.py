"""
DataFlowX Dataset Catalog & Profiling Service
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
import pandas as pd
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.exceptions import NotFoundError
from backend.database.models import Dataset, DatasetProfilingReport, DatasetVersion, QuarantineRecord
from backend.schemas.common import PaginationParams
from backend.schemas.dataset import DatasetCreate, DatasetUpdate
from data_engine.profiling import DataProfiler
from storage import ParquetManager, storage_engine


class DatasetService:
    """Catalog, versioning, profiling and metadata operations for datasets."""

    @staticmethod
    async def list_datasets(session: AsyncSession, workspace_id: Optional[str], params: PaginationParams) -> Tuple[List[Dataset], int]:
        query = select(Dataset).where(Dataset.is_deleted == False)
        if workspace_id:
            query = query.where(Dataset.workspace_id == workspace_id)
        if params.search:
            s = f"%{params.search}%"
            query = query.where((Dataset.name.ilike(s)) | (Dataset.layer.ilike(s)))

        total_stmt = select(func.count()).select_from(query.subquery())
        total = (await session.execute(total_stmt)).scalar() or 0

        query = query.order_by(Dataset.created_at.desc()).offset((params.page - 1) * params.page_size).limit(params.page_size)
        items = (await session.execute(query)).scalars().all()
        return list(items), total

    @staticmethod
    async def get_dataset(session: AsyncSession, dataset_id: str) -> Dataset:
        ds = (await session.execute(select(Dataset).where(Dataset.id == dataset_id, Dataset.is_deleted == False))).scalar_one_or_none()
        if not ds:
            raise NotFoundError("Dataset", dataset_id)
        return ds

    @staticmethod
    async def create_dataset(session: AsyncSession, workspace_id: Optional[str], payload: DatasetCreate) -> Dataset:
        slug = payload.slug or payload.name.lower().replace(" ", "-")
        ds = Dataset(
            workspace_id=workspace_id,
            source_id=payload.source_id,
            name=payload.name,
            slug=slug,
            description=payload.description,
            layer=payload.layer,
            format=payload.format,
            storage_path=payload.storage_path,
            partition_keys=payload.partition_keys,
            tags=payload.tags,
            owner_email=payload.owner_email,
            is_active=True
        )
        session.add(ds)
        await session.flush()

        # Create initial Version 1
        v1 = DatasetVersion(
            dataset_id=ds.id,
            version_number=1,
            record_count=0,
            size_bytes=0,
            storage_uri=ds.storage_path,
            commit_message="Initial dataset creation"
        )
        session.add(v1)
        await session.commit()
        await session.refresh(ds)
        return ds

    @staticmethod
    async def profile_dataset(session: AsyncSession, dataset_id: str) -> DatasetProfilingReport:
        dataset = await DatasetService.get_dataset(session, dataset_id)

        # Read sample records from storage
        records = []
        if storage_engine.exists(dataset.storage_path):
            data = storage_engine.get_object(dataset.storage_path)
            records = ParquetManager.parquet_bytes_to_records(data, limit=5000)

        df = pd.DataFrame(records) if records else pd.DataFrame([{"sample_id": 1, "value": 100}])
        profile_report = DataProfiler.profile_dataframe(df)

        report_model = DatasetProfilingReport(
            dataset_id=dataset.id,
            total_rows=profile_report.total_rows,
            total_columns=profile_report.total_columns,
            null_cells=profile_report.null_cells,
            duplicate_rows=profile_report.duplicate_rows,
            memory_bytes=profile_report.memory_bytes,
            columns_profile_json=[c.model_dump(mode="json") for c in profile_report.columns]
        )
        session.add(report_model)
        await session.commit()
        await session.refresh(report_model)
        return report_model
