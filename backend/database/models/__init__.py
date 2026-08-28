"""
DataFlowX Database Models Exporter
Aggregates and registers all SQLAlchemy models for Alembic metadata discovery.
"""

from backend.core.database import Base
from backend.database.models.base import SoftDeleteMixin, TenantMixin, TimestampMixin, UUIDPrimaryKeyMixin
from backend.database.models.dataset import (
    Dataset,
    DatasetProfilingReport,
    DatasetVersion,
    QuarantineRecord,
    SchemaColumn,
    SchemaDiff,
    SchemaModel,
    SchemaVersion,
)
from backend.database.models.execution import (
    DistributedLock,
    Execution,
    ExecutionMetric,
    TaskExecution,
    TaskLog,
    WorkerHeartbeat,
)
from backend.database.models.lineage import (
    DataContract,
    EntityTag,
    LineageEdge,
    LineageEvent,
    LineageNode,
    TagDefinition,
)
from backend.database.models.monitoring import (
    AlertIncident,
    AlertNotification,
    AlertRule,
    AuditLog,
    NotificationTemplate,
    SystemMetric,
)
from backend.database.models.organization import (
    Organization,
    Team,
    TeamMember,
    Workspace,
    WorkspaceInvitation,
    WorkspaceMember,
)
from backend.database.models.pipeline import (
    Pipeline,
    PipelineEdge,
    PipelineNode,
    PipelineParameter,
    PipelineSchedule,
    PipelineTrigger,
    PipelineVersion,
)
from backend.database.models.quality import (
    QualityCheck,
    QualityResult,
    QualityRuleDefinition,
    QualitySuite,
)
from backend.database.models.source import (
    ConnectionHealthLog,
    DataSource,
    SourceCredential,
    SourceSchemaSnapshot,
)
from backend.database.models.user import (
    ApiKey,
    PasswordReset,
    Permission,
    Role,
    RolePermission,
    User,
    UserRole,
    UserSession,
)

from backend.database.models.governance import (
    CatalogAssetModel,
    GlossaryTermModel,
    DataContractModel,
)

__all__ = [
    "Base",
    "UUIDPrimaryKeyMixin",
    "TimestampMixin",
    "SoftDeleteMixin",
    "TenantMixin",
    "User",
    "Role",
    "Permission",
    "RolePermission",
    "UserRole",
    "UserSession",
    "PasswordReset",
    "ApiKey",
    "Organization",
    "Workspace",
    "WorkspaceMember",
    "WorkspaceInvitation",
    "Team",
    "TeamMember",
    "DataSource",
    "SourceCredential",
    "ConnectionHealthLog",
    "SourceSchemaSnapshot",
    "Dataset",
    "DatasetVersion",
    "SchemaModel",
    "SchemaVersion",
    "SchemaColumn",
    "SchemaDiff",
    "DatasetProfilingReport",
    "QuarantineRecord",
    "Pipeline",
    "PipelineVersion",
    "PipelineNode",
    "PipelineEdge",
    "PipelineParameter",
    "PipelineSchedule",
    "PipelineTrigger",
    "Execution",
    "TaskExecution",
    "TaskLog",
    "ExecutionMetric",
    "WorkerHeartbeat",
    "DistributedLock",
    "QualityRuleDefinition",
    "QualitySuite",
    "QualityCheck",
    "QualityResult",
    "LineageNode",
    "LineageEdge",
    "LineageEvent",
    "DataContract",
    "TagDefinition",
    "EntityTag",
    "AlertRule",
    "AlertIncident",
    "AlertNotification",
    "NotificationTemplate",
    "AuditLog",
    "SystemMetric",
    "CatalogAssetModel",
    "GlossaryTermModel",
    "DataContractModel",
]
