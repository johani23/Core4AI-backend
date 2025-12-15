# ============================================================
# 🔥 heatmap_engine.py — Core4.AI Engine Layer 2 (Final)
# ------------------------------------------------------------
# Purpose:
#   Generate performance heatmaps for competitor price comparison
# ============================================================

class HeatmapEngine:
    def __init__(self):
        pass

    def build_heatmap(self, competitors, selected_price):
        """
        competitors: list of dicts [{ "competitor": str, "price": float }, ...]
        selected_price: float
        returns heatmap points for frontend visualization
        """

        points = []
        for c in competitors:
            comp_price = float(c["price"])
            diff = abs(selected_price - comp_price)

            # Normalized score: lower difference → hotter
            if selected_price == 0:
                score = 0
            else:
                score = max(0, 1 - (diff / selected_price))

            points.append({
                "competitor": c["competitor"],
                "price": comp_price,
                "score": round(score, 2),
                "label": self.classify_cell(score)
            })

        return points

    def classify_cell(self, value):
        if value >= 0.8: return "Hot"
        if value >= 0.5: return "Warm"
        return "Cold"
