"""
DataFlowX Distributed Saga & Compensating Transaction Orchestrator
Executes multi-step distributed pipeline workflows with forward execution and backward compensating rollbacks upon failure.
"""

from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class SagaStep(BaseModel):
    name: str
    is_executed: bool = False
    is_compensated: bool = False


class DistributedSagaOrchestrator:
    """Orchestrates distributed forward steps and compensating rollbacks."""

    def __init__(self, saga_id: str):
        self.saga_id = saga_id
        self.steps: List[SagaStep] = []
        self._actions: List[Callable[[], bool]] = []
        self._compensations: List[Callable[[], None]] = []

    def add_step(self, name: str, action: Callable[[], bool], compensation: Callable[[], None]) -> None:
        self.steps.append(SagaStep(name=name))
        self._actions.append(action)
        self._compensations.append(compensation)

    def execute_saga(self) -> bool:
        logger.info(f"Executing Saga '{self.saga_id}' with {len(self.steps)} steps")
        executed_indices = []

        for i, (step, action) in enumerate(zip(self.steps, self._actions)):
            try:
                success = action()
                if not success:
                    raise RuntimeError(f"Step '{step.name}' returned failure status")
                step.is_executed = True
                executed_indices.append(i)
            except Exception as e:
                logger.error(f"Saga '{self.saga_id}' failed at step '{step.name}': {e}. Initiating compensation rollbacks...")
                # Compensate in reverse order
                for comp_idx in reversed(executed_indices):
                    comp_step = self.steps[comp_idx]
                    comp_fn = self._compensations[comp_idx]
                    try:
                        comp_fn()
                        comp_step.is_compensated = True
                        logger.info(f"Compensated step '{comp_step.name}' successfully")
                    except Exception as comp_err:
                        logger.critical(f"Compensation failed for step '{comp_step.name}': {comp_err}")
                return False

        logger.info(f"Saga '{self.saga_id}' completed all steps successfully")
        return True
