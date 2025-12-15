# ============================================================
# 🧾 budget_engine.py — Core4.AI Engine Layer 2
# ------------------------------------------------------------
# Purpose:
#   Budget allocation optimization
# ============================================================

class BudgetEngine:
    def __init__(self):
        pass

    def allocate(self, total_budget, weights: dict):
        allocation = {}
        for channel, weight in weights.items():
            allocation[channel] = round(total_budget * weight, 2)
        return allocation
