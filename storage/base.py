"""
DataFlowX Storage Layer Base Interface
Provides unified object and file storage abstraction for Medallion Data Lakes.
"""

from abc import ABC, abstractmethod
from typing import BinaryIO, List, Optional, Union


class BaseObjectStore(ABC):
    """Abstract object storage interface."""

    @abstractmethod
    def put_object(self, key: str, data: Union[bytes, BinaryIO], content_type: Optional[str] = None) -> str:
        """Upload raw data to storage location and return URI."""
        pass

    @abstractmethod
    def get_object(self, key: str) -> bytes:
        """Download raw data bytes from storage location."""
        pass

    @abstractmethod
    def delete_object(self, key: str) -> bool:
        """Delete an object from storage."""
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        """Check if an object exists."""
        pass

    @abstractmethod
    def list_objects(self, prefix: str = "") -> List[str]:
        """List object keys matching a prefix."""
        pass

    @abstractmethod
    def get_full_path(self, key: str) -> str:
        """Get absolute path or URI for underlying access."""
        pass
