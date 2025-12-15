# ============================================================
# 🛠️ autopilot_engine.py — Core4.AI Layer 3
# ------------------------------------------------------------
# Purpose:
#   Auto-select best content strategy based on analytics
# ============================================================

class AutoPilotEngine:
    def __init__(self, success_engine, scaling_engine):
        self.success_engine = success_engine
        self.scaling_engine = scaling_engine

    def recommend(self, quality_score: float, fit_score: float, roi: float):
        success_prob = self.success_engine.predict(quality_score, fit_score)
        scalability = self.scaling_engine.score(roi, fit_score)

        if success_prob > 0.8 and scalability > 1.0:
            return "Scale aggressively"
        elif success_prob > 0.6:
            return "Publish and test"
        return "Do not publish now"

    def next_steps(self, recommendation: str):
        if recommendation == "Scale aggressively":
            return ["Boost budget", "Create more variations", "Use strongest persona"]
        if recommendation == "Publish and test":
            return ["A/B test captions", "Try different hooks"]
        return ["Revise content", "Rework narrative"]
