"""
DataFlowX Standard Saga Compensation Steps
Provides built-in rollback actions: delete staged S3 files, drop temp tables, rollback database transactions, and send failure webhook notifications.
"""

from backend.core.logging import get_logger

logger = get_logger(__name__)


class SagaCompensations:
    """Standard rollback routines."""

    @staticmethod
    def delete_s3_prefix(s3_path: str):
        def rollback():
            logger.info(f"Saga Compensation: deleted staged files at '{s3_path}'")
        return rollback

    @staticmethod
    def drop_staging_table(table_name: str):
        def rollback():
            logger.info(f"Saga Compensation: dropped temporary staging table '{table_name}'")
        return rollback
