# ============================================================
# 🧬 persona_engine.py — Core4.AI Engine Layer 1
# ------------------------------------------------------------
# Purpose:
#   - Define persona clusters
#   - Used by narrative, audiencefit, channelmix, tone_engine
# ============================================================

from typing import Dict, Any


class PersonaEngine:
    def __init__(self):
        self.personas = {
            "Adventurer": {"risk": 0.9, "novelty": 0.85, "price_sensitivity": 0.3},
            "Techy": {"risk": 0.7, "novelty": 0.95, "price_sensitivity": 0.4},
            "Fashionist": {"risk": 0.5, "novelty": 0.75, "price_sensitivity": 0.6},
            "EventGoer": {"risk": 0.4, "novelty": 0.65, "price_sensitivity": 0.5},
        }

    def match_persona(self, attributes: Dict[str, float]) -> str:
        best = None
        best_score = -1

        for persona, params in self.personas.items():
            score = 0
            for key in params:
                if key in attributes:
                    score += (1 - abs(params[key] - attributes[key]))
            if score > best_score:
                best_score = score
                best = persona

        return best

    def persona_profile(self, persona: str) -> Dict[str, Any]:
        return {
            "persona": persona,
            "traits": self.personas.get(persona, {})
        }
