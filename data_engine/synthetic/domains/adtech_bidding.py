"""
DataFlowX AdTech Programmatic RTB (Real-Time Bidding) Benchmark Generator
Generates OpenRTB 2.5 auction logs: auction IDs, publisher domains, CPM bid prices, winning prices, and click-through flags.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd


class AdTechBiddingGenerator:
    """Generates synthetic programmatic bidding events."""

    DOMAINS = ["techcrunch.com", "nytimes.com", "espn.com", "forbes.com", "bloomberg.com", "reddit.com"]
    AD_FORMATS = ["300x250_MEDIUM_RECTANGLE", "728x90_LEADERBOARD", "300x600_HALF_PAGE", "1920x1080_VIDEO"]
    GEOS = ["US", "GB", "DE", "FR", "CA", "AU", "JP"]

    @classmethod
    def generate_bids(cls, num_auctions: int = 50000) -> pd.DataFrame:
        auction_ids = [f"auc_{i:08x}" for i in range(num_auctions)]
        domains = np.random.choice(cls.DOMAINS, size=num_auctions)
        formats = np.random.choice(cls.AD_FORMATS, size=num_auctions)
        geos = np.random.choice(cls.GEOS, size=num_auctions)

        bid_cpm = np.round(np.random.gamma(shape=2.0, scale=1.5, size=num_auctions) + 0.20, 2)
        win_cpm = np.round(bid_cpm * np.random.uniform(0.70, 0.98, size=num_auctions), 2)
        clicked = np.random.binomial(n=1, p=0.018, size=num_auctions)  # 1.8% CTR

        now = datetime.now(timezone.utc)
        timestamps = [now - timedelta(seconds=int(i * 2)) for i in range(num_auctions)]

        return pd.DataFrame({
            "auction_id": auction_ids,
            "publisher_domain": domains,
            "ad_format": formats,
            "user_country": geos,
            "bid_cpm_usd": bid_cpm,
            "clearing_price_usd": win_cpm,
            "is_clicked": clicked,
            "timestamp": [ts.isoformat() for ts in timestamps]
        })
