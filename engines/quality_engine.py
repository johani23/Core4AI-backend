# ============================================================
# ⭐ quality_engine.py — Core4.AI Engine Layer 2
# ------------------------------------------------------------
# Purpose:
#   - Content quality scoring
#   - Used later by success_engine and narrative_engine
# ============================================================

from typing import Dict


class QualityEngine:
    def __init__(self):
        self.weights = {
            "clarity": 0.25,
            "visual": 0.25,
            "message_strength": 0.25,
            "brand_alignment": 0.25
        }

    def score(self, metrics: Dict[str, float]):
        total = 0
        for key, weight in self.weights.items():
            total += metrics.get(key, 0) * weight
        return round(total, 3)

    def classify(self, score: float):
        if score >= 0.8:
            return "Excellent"
        elif score >= 0.6:
            return "Good"
        elif score >= 0.4:
            return "Average"
        return "Weak"
