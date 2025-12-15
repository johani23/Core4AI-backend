# ============================================================
# 📝 narrative_engine.py — Core4.AI Layer 3
# ------------------------------------------------------------
# Purpose:
#   Generate narrative angles, hooks, and content storylines
#   Depends on: persona_engine, tone_engine, audiencefit_engine, feature_engine
# ============================================================

import random


class NarrativeEngine:
    def __init__(self, persona_engine, tone_engine, audiencefit_engine, feature_engine):
        self.persona_engine = persona_engine
        self.tone_engine = tone_engine
        self.audiencefit_engine = audiencefit_engine
        self.feature_engine = feature_engine

    def generate_hook(self, tone: str):
        tone_profile = self.tone_engine.get_tone(tone)
        keyword = random.choice(tone_profile["keywords"])
        return f"{keyword.capitalize()} your moment."

    def storyline(self, product_info: dict, persona_attributes: dict, tone: str):
        fit = self.audiencefit_engine.compute_fit(product_info["features"], persona_attributes)
        persona = fit["persona"]
        tone_profile = self.tone_engine.get_tone(tone)

        strengths = self.feature_engine.top_features(product_info["features"])
        top_feature = strengths[0][0].replace("_", " ").title()

        return {
            "persona": persona,
            "tone": tone_profile["style"],
            "hook": self.generate_hook(tone),
            "narrative": f"This product stands out with its {top_feature}. "
                         f"It naturally aligns with {persona}'s lifestyle, "
                         f"making it a perfect match.",
            "fit_score": fit["fit_score"]
        }
