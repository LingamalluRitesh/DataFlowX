"""
DataFlowX Machine Learning Model Lineage & Artifact Registry
Tracks model training artifacts, hyperparameters, dataset snapshot versions, ROC-AUC / F1 metrics, and production deployment stages.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ModelArtifact(BaseModel):
    model_id: str
    model_name: str
    version: str
    training_dataset_snapshot: str
    hyperparameters: Dict[str, Any] = Field(default_factory=dict)
    evaluation_metrics: Dict[str, float] = Field(default_factory=dict)  # roc_auc, f1_score, accuracy, mape
    deployment_stage: str = "STAGING"  # EXPERIMENT, STAGING, PRODUCTION, ARCHIVED
    registered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ModelRegistry:
    """Manages ML model artifacts and lineage."""

    def __init__(self):
        self.models: Dict[str, List[ModelArtifact]] = {}

    def register_model(self, artifact: ModelArtifact) -> ModelArtifact:
        if artifact.model_name not in self.models:
            self.models[artifact.model_name] = []
        self.models[artifact.model_name].append(artifact)
        return artifact

    def promote_model_to_production(self, model_name: str, version: str) -> bool:
        if model_name not in self.models:
            return False

        for m in self.models[model_name]:
            if m.version == version:
                m.deployment_stage = "PRODUCTION"
            elif m.deployment_stage == "PRODUCTION":
                m.deployment_stage = "ARCHIVED"

        return True
