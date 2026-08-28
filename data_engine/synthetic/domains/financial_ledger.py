"""
DataFlowX Double-Entry Financial Ledger Benchmark Generator
Generates balanced General Ledger accounting journal entries with debits, credits, account numbers, and currency ISO codes.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd


class FinancialLedgerGenerator:
    """Generates synthetic double-entry financial ledger records."""

    ACCOUNTS = [
        ("1010", "Cash & Cash Equivalents", "ASSET"),
        ("1200", "Accounts Receivable", "ASSET"),
        ("2010", "Accounts Payable", "LIABILITY"),
        ("4010", "Gross Sales Revenue", "REVENUE"),
        ("5010", "Cost of Goods Sold (COGS)", "EXPENSE"),
        ("6010", "Cloud Infrastructure Hosting", "EXPENSE"),
    ]

    @classmethod
    def generate_journal_entries(cls, num_transactions: int = 25000) -> pd.DataFrame:
        journal_ids = np.arange(100000, 100000 + num_transactions)
        amounts = np.round(np.random.exponential(scale=1500.0, size=num_transactions) + 10.0, 2)

        records = []
        now = datetime.now(timezone.utc)

        for j_id, amt in zip(journal_ids, amounts):
            tx_time = (now - timedelta(minutes=int(j_id % 10000))).isoformat()

            # Debit Entry
            records.append({
                "journal_id": f"JE-{j_id}",
                "entry_line": 1,
                "account_number": "1010",
                "account_name": "Cash & Cash Equivalents",
                "entry_type": "DEBIT",
                "amount": amt,
                "currency": "USD",
                "posted_at": tx_time
            })

            # Credit Entry
            records.append({
                "journal_id": f"JE-{j_id}",
                "entry_line": 2,
                "account_number": "4010",
                "account_name": "Gross Sales Revenue",
                "entry_type": "CREDIT",
                "amount": amt,
                "currency": "USD",
                "posted_at": tx_time
            })

        return pd.DataFrame(records)
