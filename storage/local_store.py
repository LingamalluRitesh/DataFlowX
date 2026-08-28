"""
DataFlowX Local Filesystem Storage Adapter
Provides thread-safe atomic writes and partition path resolution on local disk.
"""

import os
import shutil
import tempfile
from typing import BinaryIO, List, Optional, Union
from backend.core.exceptions import StorageError
from backend.core.logging import get_logger
from storage.base import BaseObjectStore

logger = get_logger(__name__)


class LocalFileStore(BaseObjectStore):
    """Local filesystem implementation of BaseObjectStore."""

    def __init__(self, base_path: str = "./storage"):
        self.base_path = os.path.abspath(base_path)
        os.makedirs(self.base_path, exist_ok=True)
        # Ensure medallion subdirectories exist
        for layer in ("bronze", "silver", "gold", "quarantine", "warehouse", "temp"):
            os.makedirs(os.path.join(self.base_path, layer), exist_ok=True)

    def _resolve_path(self, key: str) -> str:
        clean_key = key.lstrip("/\\")
        full_path = os.path.abspath(os.path.join(self.base_path, clean_key))
        if not full_path.startswith(self.base_path):
            raise StorageError(f"Directory traversal attack detected: {key}")
        return full_path

    def put_object(self, key: str, data: Union[bytes, BinaryIO], content_type: Optional[str] = None) -> str:
        target_path = self._resolve_path(key)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        # Atomic write via temporary file
        dir_name = os.path.dirname(target_path)
        with tempfile.NamedTemporaryFile(dir=dir_name, delete=False) as tmp:
            tmp_name = tmp.name
            if isinstance(data, bytes):
                tmp.write(data)
            else:
                shutil.copyfileobj(data, tmp)

        shutil.move(tmp_name, target_path)
        return target_path

    def get_object(self, key: str) -> bytes:
        target_path = self._resolve_path(key)
        if not os.path.exists(target_path):
            raise StorageError(f"Object not found: {key}", path=target_path)
        with open(target_path, "rb") as f:
            return f.read()

    def delete_object(self, key: str) -> bool:
        target_path = self._resolve_path(key)
        if os.path.exists(target_path):
            if os.path.isdir(target_path):
                shutil.rmtree(target_path)
            else:
                os.remove(target_path)
            return True
        return False

    def exists(self, key: str) -> bool:
        target_path = self._resolve_path(key)
        return os.path.exists(target_path)

    def list_objects(self, prefix: str = "") -> List[str]:
        target_prefix = self._resolve_path(prefix)
        matched_keys: List[str] = []

        if not os.path.exists(target_prefix):
            return []

        if os.path.isfile(target_prefix):
            rel = os.path.relpath(target_prefix, self.base_path).replace("\\", "/")
            return [rel]

        for root, _, files in os.walk(target_prefix):
            for file in files:
                abs_f = os.path.join(root, file)
                rel = os.path.relpath(abs_f, self.base_path).replace("\\", "/")
                matched_keys.append(rel)

        return sorted(matched_keys)

    def get_full_path(self, key: str) -> str:
        return self._resolve_path(key)
