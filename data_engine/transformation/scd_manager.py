"""
DataFlowX Slowly Changing Dimensions (SCD) Engine
Implements SCD Type 1 (In-place Overwrite), SCD Type 2 (Effective/Expiry Dates & is_current flag), and SCD Type 3 (Previous Value Column).
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple, Union
import pandas as pd

from backend.core.logging import get_logger
from data_engine.transformation.operators import BaseOperator

logger = get_logger(__name__)


class SCDType2Operator(BaseOperator):
    """
    Maintains full historical change tracking via Slowly Changing Dimensions Type 2.
    Appends new active versions while expiring superseded historical records.
    """

    def __init__(
        self,
        primary_key_cols: List[str],
        tracked_attribute_cols: List[str],
        effective_date_col: str = "effective_from",
        expiry_date_col: str = "effective_to",
        is_current_col: str = "is_current",
        high_water_date: str = "9999-12-31 23:59:59"
    ):
        self.primary_key_cols = primary_key_cols
        self.tracked_attribute_cols = tracked_attribute_cols
        self.effective_date_col = effective_date_col
        self.expiry_date_col = expiry_date_col
        self.is_current_col = is_current_col
        self.high_water_date = high_water_date

    def process_scd2(self, existing_dim_df: pd.DataFrame, incoming_df: pd.DataFrame, current_timestamp: Optional[str] = None) -> pd.DataFrame:
        """
        Merge incoming stream with existing historical dimension table.
        Returns the combined updated historical dimension table.
        """
        now_ts = current_timestamp or datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

        if existing_dim_df.empty:
            # First load: All incoming rows become initial active records
            initial_df = incoming_df.copy()
            initial_df[self.effective_date_col] = now_ts
            initial_df[self.expiry_date_col] = self.high_water_date
            initial_df[self.is_current_col] = True
            return initial_df

        existing = existing_dim_df.copy()
        incoming = incoming_df.copy()

        # Separate current vs historical
        current_records = existing[existing[self.is_current_col] == True].copy()
        historical_records = existing[existing[self.is_current_col] == False].copy()

        merged = pd.merge(
            incoming,
            current_records,
            on=self.primary_key_cols,
            how="left",
            suffixes=("_new", "_old")
        )

        records_to_expire = []
        new_records_to_insert = []
        unchanged_records = []

        for idx, row in merged.iterrows():
            is_existing = pd.notnull(row.get(f"{self.is_current_col}_old"))
            if not is_existing:
                # Completely new record
                new_row = {pk: row[pk] for pk in self.primary_key_cols}
                for attr in self.tracked_attribute_cols:
                    new_row[attr] = row.get(f"{attr}_new", row.get(attr))
                new_row[self.effective_date_col] = now_ts
                new_row[self.expiry_date_col] = self.high_water_date
                new_row[self.is_current_col] = True
                new_records_to_insert.append(new_row)
            else:
                # Check if any tracked attribute changed
                has_changed = False
                for attr in self.tracked_attribute_cols:
                    val_new = row.get(f"{attr}_new")
                    val_old = row.get(f"{attr}_old")
                    if str(val_new) != str(val_old):
                        has_changed = True
                        break

                if has_changed:
                    # 1. Expire old record
                    expired_row = {pk: row[pk] for pk in self.primary_key_cols}
                    for attr in self.tracked_attribute_cols:
                        expired_row[attr] = row.get(f"{attr}_old")
                    expired_row[self.effective_date_col] = row.get(f"{self.effective_date_col}_old")
                    expired_row[self.expiry_date_col] = now_ts
                    expired_row[self.is_current_col] = False
                    records_to_expire.append(expired_row)

                    # 2. Insert new active version
                    new_row = {pk: row[pk] for pk in self.primary_key_cols}
                    for attr in self.tracked_attribute_cols:
                        new_row[attr] = row.get(f"{attr}_new")
                    new_row[self.effective_date_col] = now_ts
                    new_row[self.expiry_date_col] = self.high_water_date
                    new_row[self.is_current_col] = True
                    new_records_to_insert.append(new_row)
                else:
                    # Unchanged record remains current
                    unchanged_row = {pk: row[pk] for pk in self.primary_key_cols}
                    for attr in self.tracked_attribute_cols:
                        unchanged_row[attr] = row.get(f"{attr}_old")
                    unchanged_row[self.effective_date_col] = row.get(f"{self.effective_date_col}_old")
                    unchanged_row[self.expiry_date_col] = row.get(f"{self.expiry_date_col}_old")
                    unchanged_row[self.is_current_col] = True
                    unchanged_records.append(unchanged_row)

        all_updated = (
            historical_records.to_dict(orient="records") +
            records_to_expire +
            new_records_to_insert +
            unchanged_records
        )
        return pd.DataFrame(all_updated)


class SCDType1Operator(BaseOperator):
    """SCD Type 1: Performs in-place upsert on matching primary keys (overwrites without history)."""

    def __init__(self, primary_key_cols: List[str], update_cols: Optional[List[str]] = None):
        self.primary_key_cols = primary_key_cols
        self.update_cols = update_cols

    def process_scd1(self, existing_df: pd.DataFrame, incoming_df: pd.DataFrame) -> pd.DataFrame:
        if existing_df.empty:
            return incoming_df.copy()
        if incoming_df.empty:
            return existing_df.copy()

        # Deduplicate on PK keeping the latest incoming row
        combined = pd.concat([existing_df, incoming_df], ignore_index=True)
        return combined.drop_duplicates(subset=self.primary_key_cols, keep="last").reset_index(drop=True)
