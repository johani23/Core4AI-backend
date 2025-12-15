# ============================================================
# 🚦 readiness_engine.py — Core4.AI Layer 3
# ------------------------------------------------------------
# Purpose:
#   Determine if a piece of content is ready for publishing
# ============================================================

class ReadinessEngine:
    def __init__(self, success_engine, quality_engine):
        self.success_engine = success_engine
        self.quality_engine = quality_engine

    def evaluate(self, quality_score: float, fit_score: float):
        success_prob = self.success_engine.predict(quality_score, fit_score)

        if quality_score > 0.7 and success_prob > 0.65:
            return "Ready"
        elif quality_score > 0.5:
            return "Needs Optimization"
        return "Not Ready"
