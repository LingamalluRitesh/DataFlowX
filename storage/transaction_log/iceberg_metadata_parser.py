"""
DataFlowX Apache Iceberg Table Metadata JSON Parser
Parses Apache Iceberg table metadata specs (v1/v2), snapshot histories, manifest lists, and partition specs.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class IcebergSnapshotSpec(BaseModel):
    snapshot_id: int
    parent_snapshot_id: Optional[int] = None
    timestamp_ms: int
    manifest_list: str
    summary: Dict[str, str] = Field(default_factory=dict)


class IcebergTableMetadata(BaseModel):
    format_version: int = 2
    table_uuid: str
    location: str
    last_sequence_number: int = 0
    last_updated_ms: int
    current_snapshot_id: Optional[int] = None
    snapshots: List[IcebergSnapshotSpec] = Field(default_factory=list)


class IcebergMetadataParser:
    """Parses Iceberg table metadata JSON files."""

    @classmethod
    def parse_metadata_dict(cls, data: Dict[str, Any]) -> IcebergTableMetadata:
        snaps = []
        for s in data.get("snapshots", []):
            snaps.append(IcebergSnapshotSpec(
                snapshot_id=s.get("snapshot-id", 0),
                parent_snapshot_id=s.get("parent-snapshot-id"),
                timestamp_ms=s.get("timestamp-ms", 0),
                manifest_list=s.get("manifest-list", ""),
                summary=s.get("summary", {})
            ))

        return IcebergTableMetadata(
            format_version=data.get("format-version", 2),
            table_uuid=data.get("table-uuid", "default-uuid"),
            location=data.get("location", ""),
            last_sequence_number=data.get("last-sequence-number", 0),
            last_updated_ms=data.get("last-updated-ms", 0),
            current_snapshot_id=data.get("current-snapshot-id"),
            snapshots=snaps
        )
