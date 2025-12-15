# ============================================================
# success_engine.py
# ============================================================

from math import exp

class SuccessEngine:
    def __init__(self, quality_engine, audience_fit_engine):
        self.quality_engine = quality_engine
        self.audience_fit_engine = audience_fit_engine

    def predict(self, quality_score, fit_score):
        prob = 1 / (1 + exp(-(3 * quality_score + 2.5 * fit_score - 3)))
        return round(prob, 2)

    def classify(self, prob):
        if prob > 0.75:
            return "high"
        if prob > 0.4:
            return "medium"
        return "low"
