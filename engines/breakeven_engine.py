# ============================================================
# ⚖️ breakeven_engine.py — Core4.AI Engine Layer 2
# ------------------------------------------------------------
# Purpose:
#   Break-even price & units calculation
# ============================================================

class BreakEvenEngine:
    def __init__(self):
        pass

    def breakeven_units(self, fixed_costs: float, margin_per_unit: float):
        if margin_per_unit <= 0:
            return None
        return round(fixed_costs / margin_per_unit)

    def breakeven_price(self, cost: float, margin_target: float):
        return round(cost * (1 + margin_target), 2)
