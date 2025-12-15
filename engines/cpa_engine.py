# ============================================================
# 🎯 cpa_engine.py — Core4.AI Engine Layer 2
# ------------------------------------------------------------
# Purpose:
#   Calculate Cost Per Acquisition
# ============================================================

class CPAEngine:
    def __init__(self):
        pass

    def compute(self, spend: float, acquisitions: int):
        if acquisitions == 0:
            return None
        return round(spend / acquisitions, 3)
