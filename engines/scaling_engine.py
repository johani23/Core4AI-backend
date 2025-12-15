# ============================================================
# 📈 scaling_engine.py — Core4.AI Engine Layer 2
# ------------------------------------------------------------
# Purpose:
#   Estimate scaling potential based on ROI + audience fit
# ============================================================

class ScalingEngine:
    def __init__(self):
        pass

    def score(self, roi: float, fit: float):
        return round((roi * 0.6) + (fit * 0.4), 3)

    def classify(self, score: float):
        if score > 1.2:
            return "High Scalability"
        elif score > 0.8:
            return "Moderate Scalability"
        return "Low Scalability"
