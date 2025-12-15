# ============================================================
# 💼 competitor_db.py — Core4.AI Engine Layer 1
# ------------------------------------------------------------
# Purpose:
#   - Provide market & competitor reference data
#   - Core dependency for: pricing_engine, ROI, funnel, scaling
# ============================================================

import statistics
from typing import List, Dict, Optional


class CompetitorDB:
    def __init__(self):
        # Mocked competitor DB — replace later with actual API/SQL connector
        self.data = {}

    def insert_product(self, category: str, competitor_name: str, price: float):
        self.data.setdefault(category, [])
        self.data[category].append({
            "competitor": competitor_name,
            "price": price
        })

    def get_prices(self, category: str) -> List[float]:
        if category not in self.data:
            return []
        return [item["price"] for item in self.data[category]]

    def avg_price(self, category: str) -> Optional[float]:
        prices = self.get_prices(category)
        return statistics.mean(prices) if prices else None

    def min_max_price(self, category: str):
        prices = self.get_prices(category)
        if not prices:
            return None, None
        return min(prices), max(prices)

    def price_gap(self, category: str, our_price: float) -> Optional[float]:
        avg = self.avg_price(category)
        if avg is None:
            return None
        return our_price - avg

    def summary(self, category: str) -> Dict:
        prices = self.get_prices(category)
        if not prices:
            return {"status": "no competitor data"}

        return {
            "competitors_count": len(prices),
            "avg_price": statistics.mean(prices),
            "min": min(prices),
            "max": max(prices),
        }
