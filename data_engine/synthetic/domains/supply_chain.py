"""
DataFlowX Supply Chain Logistics & Inventory Benchmark Generator
Generates warehouse SKU stock movements, reorder point alerts, supplier lead times, and carrier tracking waybills.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd


class SupplyChainGenerator:
    """Generates synthetic warehouse inventory and shipment records."""

    WAREHOUSES = ["WH-EAST-NJ", "WH-WEST-CA", "WH-CENTRAL-TX", "WH-EU-NL", "WH-APAC-SG"]
    CARRIERS = ["FedEx Express", "UPS Ground", "DHL Global", "USPS Priority", "Maersk Ocean"]

    @classmethod
    def generate_shipments(cls, num_shipments: int = 30000) -> pd.DataFrame:
        tracking_numbers = [f"TRK{900000000+i}" for i in range(num_shipments)]
        warehouses = np.random.choice(cls.WAREHOUSES, size=num_shipments)
        carriers = np.random.choice(cls.CARRIERS, size=num_shipments)
        weight_kg = np.round(np.random.exponential(scale=4.5, size=num_shipments) + 0.1, 2)
        shipping_cost = np.round(weight_kg * np.random.uniform(3.5, 7.0, size=num_shipments) + 5.0, 2)

        now = datetime.now(timezone.utc)
        timestamps = [now - timedelta(hours=int(i % 500)) for i in range(num_shipments)]

        return pd.DataFrame({
            "tracking_number": tracking_numbers,
            "origin_warehouse": warehouses,
            "carrier_service": carriers,
            "package_weight_kg": weight_kg,
            "shipping_fee_usd": shipping_cost,
            "dispatched_at": [ts.isoformat() for ts in timestamps]
        })
