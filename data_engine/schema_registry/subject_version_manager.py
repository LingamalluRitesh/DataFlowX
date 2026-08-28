"""
DataFlowX Schema Registry Subject Version Manager
Maintains schema subjects, versions (v1, v2, ...), global schema IDs, and MD5 fingerprint lookups.
"""

import hashlib
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from backend.core.logging import get_logger

logger = get_logger(__name__)


class RegisteredSchema(BaseModel):
    schema_id: int
    subject: str
    version: int
    schema_type: str  # AVRO, PROTOBUF, JSON
    schema_str: str
    fingerprint_md5: str


class SubjectVersionManager:
    """Manages schema registry subjects."""

    def __init__(self):
        self._subjects: Dict[str, List[RegisteredSchema]] = {}
        self._global_id_counter = 0

    def register_schema(self, subject: str, schema_type: str, schema_str: str) -> RegisteredSchema:
        md5 = hashlib.md5(schema_str.encode("utf-8")).hexdigest()
        history = self._subjects.setdefault(subject, [])

        # Check if already registered
        for s in history:
            if s.fingerprint_md5 == md5:
                return s

        self._global_id_counter += 1
        new_v = len(history) + 1
        rec = RegisteredSchema(
            schema_id=self._global_id_counter,
            subject=subject,
            version=new_v,
            schema_type=schema_type,
            schema_str=schema_str,
            fingerprint_md5=md5
        )
        history.append(rec)
        logger.info(f"Registered schema ID {rec.schema_id} for subject '{subject}' version {rec.version}")
        return rec
