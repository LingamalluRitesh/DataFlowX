"""
DataFlowX High-Throughput Synthetic Data Generator
Generates realistic multi-domain enterprise benchmark datasets: E-Commerce transactions, IoT telemetry, Financial ledgers, Healthcare patient records, and Clickstream event logs.
"""

from datetime import datetime, timedelta, timezone
import random
import time
from typing import Any, Dict, Generator, List, Optional
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field


class SyntheticDatasetGenerator:
    """Generates synthetic tabular datasets for performance benchmarks and stress tests."""

    STATUS_CHOICES = ["COMPLETED", "DELIVERED", "PROCESSING", "SHIPPED", "CANCELLED", "REFUNDED"]
    CATEGORIES = ["Electronics", "Home & Garden", "Apparel", "Beauty", "Sports", "Books", "Industrial"]
    CITIES = ["New York", "San Francisco", "London", "Berlin", "Tokyo", "Singapore", "Sydney", "Toronto"]

    @classmethod
    def generate_orders_dataframe(cls, num_rows: int = 100000, start_date: str = "2026-01-01") -> pd.DataFrame:
        start_dt = datetime.fromisoformat(start_date)
        
        # Vectorized generation using numpy for speed
        order_ids = np.arange(1000000, 1000000 + num_rows)
        customer_ids = np.random.randint(1000, 50000, size=num_rows)
        amounts = np.round(np.random.exponential(scale=75.0, size=num_rows) + 5.0, 2)
        quantities = np.random.randint(1, 10, size=num_rows)
        statuses = np.random.choice(cls.STATUS_CHOICES, size=num_rows, p=[0.5, 0.25, 0.1, 0.08, 0.05, 0.02])
        categories = np.random.choice(cls.CATEGORIES, size=num_rows)
        cities = np.random.choice(cls.CITIES, size=num_rows)

        # Generate timestamps
        seconds_offsets = np.random.randint(0, 86400 * 180, size=num_rows)
        timestamps = [start_dt + timedelta(seconds=int(s)) for s in seconds_offsets]

        return pd.DataFrame({
            "order_id": order_ids,
            "customer_id": [f"cust_{cid:05d}" for cid in customer_ids],
            "order_total": amounts,
            "quantity": quantities,
            "category": categories,
            "shipping_city": cities,
            "order_status": statuses,
            "created_at": [ts.isoformat() for ts in timestamps]
        })

    @classmethod
    def generate_iot_telemetry(cls, num_rows: int = 50000, num_devices: int = 100) -> pd.DataFrame:
        device_ids = [f"sensor-node-{i:03d}" for i in range(1, num_devices + 1)]
        chosen_devices = np.random.choice(device_ids, size=num_rows)
        temperatures = np.round(np.random.normal(loc=22.5, scale=4.0, size=num_rows), 2)
        humidity = np.round(np.random.uniform(30.0, 80.0, size=num_rows), 2)
        voltages = np.round(np.random.normal(loc=3.3, scale=0.1, size=num_rows), 3)

        now = datetime.now(timezone.utc)
        timestamps = [now - timedelta(seconds=int(i * 5)) for i in range(num_rows)]

        return pd.DataFrame({
            "device_id": chosen_devices,
            "temperature_c": temperatures,
            "humidity_pct": humidity,
            "battery_volts": voltages,
            "recorded_at": [ts.isoformat() for ts in timestamps]
        })
