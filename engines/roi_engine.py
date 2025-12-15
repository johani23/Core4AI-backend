# ============================================================
# 💰 roi_engine.py — Core4.AI Engine Layer 2
# ------------------------------------------------------------
# Purpose:
#   Compute ROI for campaigns/products
# ============================================================

class ROIEngine:
    def __init__(self):
        pass

    def compute(self, revenue: float, cost: float):
        if cost == 0:
            return 1.0
        roi = (revenue - cost) / cost
        return round(roi, 3)

    def classify(self, roi: float):
        if roi > 1:
            return "Excellent ROI"
        elif roi > 0.5:
            return "Positive ROI"
        return "Negative ROI"
