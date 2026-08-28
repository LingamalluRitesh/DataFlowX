"""
DataFlowX Apache Iceberg Table Format Manager
Manages snapshot manifests, schema evolution diffs, partition specs, and metadata JSON generation.
"""

from datetime import datetime, timezone
import json
import os
import uuid
from typing import Any, Dict, List, Optional, Tuple, Union
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class IcebergField(BaseModel):
    id: int
    name: str
    type: str
    required: bool = False
    doc: Optional[str] = None


class IcebergSchema(BaseModel):
    schema_id: int = 0
    type: str = "struct"
    fields: List[IcebergField] = Field(default_factory=list)


class IcebergPartitionField(BaseModel):
    source_id: int
    field_id: int
    name: str
    transform: str = "identity"  # identity, year, month, day, hour, bucket[N], truncate[W]


class IcebergPartitionSpec(BaseModel):
    spec_id: int = 0
    fields: List[IcebergPartitionField] = Field(default_factory=list)


class IcebergSnapshot(BaseModel):
    snapshot_id: int
    parent_snapshot_id: Optional[int] = None
    timestamp_ms: int
    manifest_list: str
    summary: Dict[str, str] = Field(default_factory=dict)


class IcebergTableMetadata(BaseModel):
    format_version: int = 2
    table_uuid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    location: str
    last_sequence_number: int = 1
    last_updated_ms: int = Field(default_factory=lambda: int(datetime.now(timezone.utc).timestamp() * 1000))
    last_column_id: int = 1
    current_schema_id: int = 0
    schemas: List[IcebergSchema] = Field(default_factory=list)
    default_spec_id: int = 0
    partition_specs: List[IcebergPartitionSpec] = Field(default_factory=list)
    current_snapshot_id: Optional[int] = None
    snapshots: List[IcebergSnapshot] = Field(default_factory=list)


class IcebergManager:
    """Enterprise Apache Iceberg Table Catalog and Metadata Manager."""

    @staticmethod
    def create_table_metadata(
        table_name: str,
        base_location: str,
        columns: List[Dict[str, Any]],
        partition_keys: Optional[List[str]] = None
    ) -> IcebergTableMetadata:
        """Construct valid Apache Iceberg v2 table metadata specification."""
        fields = []
        for idx, col in enumerate(columns, start=1):
            fields.append(IcebergField(
                id=idx,
                name=col["name"],
                type=col.get("type", "string"),
                required=col.get("required", False),
                doc=col.get("comment")
            ))

        schema = IcebergSchema(schema_id=0, fields=fields)

        partition_fields = []
        if partition_keys:
            name_to_id = {f.name: f.id for f in fields}
            for p_idx, pkey in enumerate(partition_keys, start=1000):
                if pkey in name_to_id:
                    partition_fields.append(IcebergPartitionField(
                        source_id=name_to_id[pkey],
                        field_id=p_idx,
                        name=pkey,
                        transform="identity"
                    ))

        partition_spec = IcebergPartitionSpec(spec_id=0, fields=partition_fields)

        meta = IcebergTableMetadata(
            location=f"{base_location.rstrip('/')}/{table_name}",
            last_column_id=len(fields),
            schemas=[schema],
            partition_specs=[partition_spec]
        )
        return meta

    @staticmethod
    def commit_snapshot(
        metadata: IcebergTableMetadata,
        data_files_added: List[str],
        records_added: int,
        bytes_added: int,
        operation: str = "append"
    ) -> IcebergSnapshot:
        """Create new ACID snapshot commit."""
        now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
        snapshot_id = int(uuid.uuid4().int >> 64)

        manifest_path = f"{metadata.location}/metadata/snap-{snapshot_id}.avro"
        summary = {
            "operation": operation,
            "added-data-files": str(len(data_files_added)),
            "added-records": str(records_added),
            "added-files-size": str(bytes_added),
            "total-records": str(records_added),
        }

        snapshot = IcebergSnapshot(
            snapshot_id=snapshot_id,
            parent_snapshot_id=metadata.current_snapshot_id,
            timestamp_ms=now_ms,
            manifest_list=manifest_path,
            summary=summary
        )

        metadata.snapshots.append(snapshot)
        metadata.current_snapshot_id = snapshot_id
        metadata.last_updated_ms = now_ms
        metadata.last_sequence_number += 1

        logger.info(f"Committed Iceberg snapshot {snapshot_id} (op={operation}, added={records_added} rows)")
        return snapshot
