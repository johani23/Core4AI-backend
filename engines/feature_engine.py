# ============================================================
# 🔬 feature_engine.py — Core4.AI Engine Layer 1
# ------------------------------------------------------------
# Purpose:
#   - Normalize product attributes
#   - Extract high-impact features for other engines
#   - Used heavily by: pricing, audiencefit, quality, narrative
# ============================================================

from typing import Dict, Any


class FeatureEngine:
    def __init__(self):
        self.weights = {
            "design": 0.25,
            "durability": 0.2,
            "brand": 0.15,
            "uniqueness": 0.15,
            "utility": 0.25
        }

    def normalize(self, value: float, min_v: float = 1, max_v: float = 10) -> float:
        return (value - min_v) / (max_v - min_v)

    def compute_feature_score(self, features: Dict[str, float]) -> float:
        score = 0.0
        for key, weight in self.weights.items():
            if key in features:
                score += self.normalize(features[key]) * weight
        return round(score, 3)

    def top_features(self, features: Dict[str, float]):
        sorted_items = sorted(features.items(), key=lambda x: x[1], reverse=True)
        return sorted_items[:3]

    def project_strengths(self, features: Dict[str, float]):
        return {
            "top_3_strengths": self.top_features(features),
            "overall_score": self.compute_feature_score(features)
        }
