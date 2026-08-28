"""
DataFlowX Composite Pipeline Transformer
Orchestrates sequential or conditional execution of multiple transformation steps.
"""

from typing import Any, Dict, List, Optional
import pandas as pd
from backend.core.logging import get_logger
from data_engine.transformation.custom_python import CustomPythonTransformer
from data_engine.transformation.custom_sql import CustomSQLTransformer
from data_engine.transformation.operators import (
    AggregateOperator,
    BaseOperator,
    CalculatedColumnOperator,
    CastDataTypesOperator,
    ConditionalColumnOperator,
    DeduplicateOperator,
    DropColumnsOperator,
    FillMissingOperator,
    FilterRowsOperator,
    JoinOperator,
    NormalizeStringsOperator,
    RenameColumnsOperator,
    SelectColumnsOperator,
    SortOperator,
)

logger = get_logger(__name__)


class PipelineTransformer:
    """Chains and executes composite transformations on data batches."""

    def __init__(self, steps: Optional[List[Dict[str, Any]]] = None):
        self.steps = steps or []

    def add_step(self, step_type: str, config: Dict[str, Any]) -> "PipelineTransformer":
        self.steps.append({"type": step_type, "config": config})
        return self

    def transform(self, df: pd.DataFrame, context_params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        current_df = df.copy()

        for idx, step in enumerate(self.steps):
            stype = step.get("type", "").lower()
            cfg = step.get("config", {})
            logger.debug(f"Executing transformation step {idx + 1}/{len(self.steps)}: {stype}")

            if stype == "select":
                op = SelectColumnsOperator(columns=cfg.get("columns", []))
                current_df = op.transform(current_df)
            elif stype == "rename":
                op = RenameColumnsOperator(mapping=cfg.get("mapping", {}))
                current_df = op.transform(current_df)
            elif stype == "drop":
                op = DropColumnsOperator(columns=cfg.get("columns", []))
                current_df = op.transform(current_df)
            elif stype == "cast":
                op = CastDataTypesOperator(type_mapping=cfg.get("type_mapping", {}))
                current_df = op.transform(current_df)
            elif stype == "filter":
                op = FilterRowsOperator(condition_expr=cfg.get("condition", ""))
                current_df = op.transform(current_df)
            elif stype == "deduplicate":
                op = DeduplicateOperator(subset=cfg.get("subset"), keep=cfg.get("keep", "first"))
                current_df = op.transform(current_df)
            elif stype == "normalize":
                op = NormalizeStringsOperator(
                    columns=cfg.get("columns", []),
                    case_mode=cfg.get("case_mode"),
                    strip_whitespace=cfg.get("strip_whitespace", True),
                    remove_special_chars=cfg.get("remove_special_chars", False),
                )
                current_df = op.transform(current_df)
            elif stype == "fill_missing":
                op = FillMissingOperator(strategies=cfg.get("strategies", {}))
                current_df = op.transform(current_df)
            elif stype == "calculated_column":
                op = CalculatedColumnOperator(
                    new_column_name=cfg.get("name", "new_col"),
                    expression=cfg.get("expression", "")
                )
                current_df = op.transform(current_df)
            elif stype == "conditional_column":
                op = ConditionalColumnOperator(
                    new_column_name=cfg.get("name", "status"),
                    conditions=cfg.get("conditions", []),
                    else_value=cfg.get("else_value", "Other")
                )
                current_df = op.transform(current_df)
            elif stype == "aggregate":
                op = AggregateOperator(
                    group_by=cfg.get("group_by", []),
                    aggregations=cfg.get("aggregations", {})
                )
                current_df = op.transform(current_df)
            elif stype == "sort":
                op = SortOperator(
                    by=cfg.get("by", []),
                    ascending=cfg.get("ascending", True)
                )
                current_df = op.transform(current_df)
            elif stype == "custom_sql":
                sql_op = CustomSQLTransformer(sql_query=cfg.get("query", "SELECT * FROM input_data"))
                current_df = sql_op.execute(current_df)
            elif stype == "custom_python":
                py_op = CustomPythonTransformer(
                    script_code=cfg.get("script", "df = df"),
                    timeout_seconds=cfg.get("timeout_seconds", 15)
                )
                current_df = py_op.execute(current_df, context_params=context_params)

        return current_df
