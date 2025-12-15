# ============================================================
# 🔻 funnel_engine.py — Core4.AI Engine Layer 2
# ------------------------------------------------------------
# Purpose:
#   Analyze conversions across funnel stages
# ============================================================

class FunnelEngine:
    def __init__(self):
        pass

    def compute_funnel(self, views, clicks, carts, purchases):
        return {
            "ctr": round(clicks / views, 3) if views else 0,
            "atc_rate": round(carts / clicks, 3) if clicks else 0,
            "purchase_rate": round(purchases / carts, 3) if carts else 0,
            "overall_conversion": round(purchases / views, 3) if views else 0
        }

    def classify(self, conversion):
        if conversion > 0.1:
            return "Excellent"
        elif conversion > 0.05:
            return "Good"
        return "Needs Improvement"
