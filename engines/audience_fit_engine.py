# ============================================================
# 🎯 audiencefit_engine.py — Core4.AI Engine Layer 2
# ------------------------------------------------------------
# Purpose:
#   Computes product<>persona compatibility score
#   Depends on: persona_engine, feature_engine
# ============================================================

from typing import Dict
from math import exp


class AudienceFitEngine:
    def __init__(self, persona_engine, feature_engine):
        self.persona_engine = persona_engine
        self.feature_engine = feature_engine

    def compute_fit(self, product_features: Dict[str, float], persona_attributes: Dict[str, float]):
        feature_score = self.feature_engine.compute_feature_score(product_features)
        persona = self.persona_engine.match_persona(persona_attributes)

        match_quality = 1 - abs(feature_score - persona_attributes.get("novelty", 0.5))

        fit_score = round((feature_score * 0.6) + (match_quality * 0.4), 3)

        return {
            "persona": persona,
            "feature_score": feature_score,
            "fit_score": fit_score
        }

    def audience_recommendation(self, fit_score: float):
        if fit_score > 0.8:
            return "Excellent Fit"
        elif fit_score > 0.6:
            return "Strong Fit"
        elif fit_score > 0.4:
            return "Moderate Fit"
        return "Weak Fit"
