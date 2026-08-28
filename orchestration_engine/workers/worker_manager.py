"""
DataFlowX Worker Node Health & Telemetry Manager
Monitors worker CPU, memory, active task count, and sends periodic heartbeats.
"""

from datetime import datetime, timezone
import os
import platform
import socket
import time
from typing import Any, Dict, List, Optional
from backend.core.logging import get_logger

logger = get_logger(__name__)


class WorkerNodeManager:
    """Monitors local worker node telemetry and health status."""

    def __init__(self, worker_id: Optional[str] = None):
        self.worker_id = worker_id or f"worker_{socket.gethostname()}_{os.getpid()}"
        self.hostname = socket.gethostname()
        self.ip_address = self._get_ip()
        self.system = platform.system()

    def _get_ip(self) -> str:
        try:
            return socket.gethostbyname(self.hostname)
        except Exception:
            return "127.0.0.1"

    def get_telemetry(self) -> Dict[str, Any]:
        """Gather CPU and Memory resource metrics."""
        cpu_pct = 0.0
        mem_used_mb = 0.0

        try:
            import psutil
            cpu_pct = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory()
            mem_used_mb = mem.used / (1024 * 1024)
        except ImportError:
            # Fallback if psutil is not available
            pass

        return {
            "worker_id": self.worker_id,
            "hostname": self.hostname,
            "ip_address": self.ip_address,
            "status": "active",
            "cpu_percent": round(cpu_pct, 2),
            "memory_used_mb": round(mem_used_mb, 2),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
