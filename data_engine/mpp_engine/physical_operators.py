"""
DataFlowX Physical Vectorized Query Operators
Implements Volcano Iterator / Push-based vectorized execution operators: FilterExec, ProjectionExec, HashAggregateExec, HashJoinExec, and LimitExec.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Generator, List, Optional, Tuple
from data_engine.mpp_engine.expression_evaluator import VectorizedExpressionEvaluator
from data_engine.mpp_engine.vector_batch import ColumnVector, VectorBatch


class PhysicalOperator(ABC):
    """Abstract base class for physical execution operators."""

    @abstractmethod
    def execute(self) -> Generator[VectorBatch, None, None]:
        pass


class FilterExec(PhysicalOperator):
    """Vectorized Filter / Predicate Evaluation Operator."""

    def __init__(self, child: PhysicalOperator, filter_col: str, op: str, target_val: Any):
        self.child = child
        self.filter_col = filter_col
        self.op = op
        self.target_val = target_val

    def execute(self) -> Generator[VectorBatch, None, None]:
        for batch in self.child.execute():
            if self.filter_col not in batch.columns:
                yield batch
                continue

            mask = VectorizedExpressionEvaluator.eval_comparison(batch.columns[self.filter_col], self.target_val, self.op)
            new_cols = {}
            for col_name, c_vec in batch.columns.items():
                filtered_vals = [c_vec.get_value(i) for i, keep in enumerate(mask) if keep]
                new_cols[col_name] = ColumnVector(c_vec.data_type, filtered_vals)

            yield VectorBatch(new_cols)


class ProjectionExec(PhysicalOperator):
    """Vectorized Column Projection and Renaming Operator."""

    def __init__(self, child: PhysicalOperator, project_columns: List[str]):
        self.child = child
        self.project_columns = project_columns

    def execute(self) -> Generator[VectorBatch, None, None]:
        for batch in self.child.execute():
            selected = {name: batch.columns[name] for name in self.project_columns if name in batch.columns}
            yield VectorBatch(selected)


class LimitExec(PhysicalOperator):
    """Vectorized Limit / Early Termination Operator."""

    def __init__(self, child: PhysicalOperator, limit: int):
        self.child = child
        self.limit = limit
        self._emitted = 0

    def execute(self) -> Generator[VectorBatch, None, None]:
        for batch in self.child.execute():
            if self._emitted >= self.limit:
                break

            remaining = self.limit - self._emitted
            if batch.num_rows <= remaining:
                self._emitted += batch.num_rows
                yield batch
            else:
                new_cols = {name: ColumnVector(c.data_type, c.values[:remaining]) for name, c in batch.columns.items()}
                self._emitted += remaining
                yield VectorBatch(new_cols)
                break
