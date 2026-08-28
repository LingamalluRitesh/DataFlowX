"""
DataFlowX Data Quality & Validation Models
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import BigInteger, Boolean, DateTime, Float, ForeignKey, JSON as JSONB, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.core.database import Base
from backend.database.models.base import SoftDeleteMixin, TenantMixin, TimestampMixin, UUIDPrimaryKeyMixin


class QualityRuleDefinition(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin, TenantMixin):
    """Reusable data quality rule template."""
    __tablename__ = "quality_rule_definitions"
    __table_args__ = (UniqueConstraint("workspace_id", "name", name="uq_workspace_rule_name"),)

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    rule_type: Mapped[str] = mapped_column(String(50), nullable=False)
    # Types: NOT_NULL, UNIQUE, RANGE, REGEX, EMAIL, DATA_TYPE, DATE_RANGE, FOREIGN_KEY, DUPLICATE_CHECK, CUSTOM_SQL, CUSTOM_PYTHON, COMPLETENESS
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    parameters_schema_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    default_severity: Mapped[str] = mapped_column(String(20), default="ERROR", nullable=False)  # WARNING, ERROR, CRITICAL
    is_builtin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class QualitySuite(Base, UUIDPrimaryKeyMixin, TimestampMixin, SoftDeleteMixin, TenantMixin):
    """Group of quality checks bound together to test a dataset or pipeline stage."""
    __tablename__ = "quality_suites"
    __table_args__ = (UniqueConstraint("workspace_id", "name", name="uq_workspace_suite_name"),)

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    checks: Mapped[List["QualityCheck"]] = relationship("QualityCheck", back_populates="suite", cascade="all, delete-orphan")


class QualityCheck(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Configured instance of a quality rule applied to a dataset column."""
    __tablename__ = "quality_checks"

    quality_suite_id: Mapped[str] = mapped_column(String(36), ForeignKey("quality_suites.id", ondelete="CASCADE"), nullable=False, index=True)
    rule_definition_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("quality_rule_definitions.id", ondelete="SET NULL"), nullable=True)
    dataset_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("datasets.id", ondelete="SET NULL"), nullable=True, index=True)
    rule_name: Mapped[str] = mapped_column(String(100), nullable=False)
    rule_type: Mapped[str] = mapped_column(String(50), nullable=False)
    target_column: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    condition_params: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    threshold_percentage: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)  # 0.0 to 100.0
    failure_action: Mapped[str] = mapped_column(String(30), default="FAIL_PIPELINE", nullable=False)  # FAIL_PIPELINE, WARN_AND_CONTINUE, QUARANTINE_RECORDS, SEND_ALERT
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    suite: Mapped["QualitySuite"] = relationship("QualitySuite", back_populates="checks")
    results: Mapped[List["QualityResult"]] = relationship("QualityResult", back_populates="check", cascade="all, delete-orphan")


class QualityResult(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    """Outcome and metric evaluation of a quality check during pipeline run."""
    __tablename__ = "quality_results"

    execution_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("executions.id", ondelete="CASCADE"), nullable=True, index=True)
    task_execution_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("task_executions.id", ondelete="CASCADE"), nullable=True)
    quality_check_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("quality_checks.id", ondelete="SET NULL"), nullable=True)
    dataset_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("datasets.id", ondelete="SET NULL"), nullable=True)

    rule_name: Mapped[str] = mapped_column(String(100), nullable=False)
    rule_type: Mapped[str] = mapped_column(String(50), nullable=False)
    target_column: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)

    total_records: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    passed_records: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    failed_records: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    quarantined_records: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)

    score_percentage: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)
    passed: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    details_json: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    check: Mapped[Optional["QualityCheck"]] = relationship("QualityCheck", back_populates="results")
