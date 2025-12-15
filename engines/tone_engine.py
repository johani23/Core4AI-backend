# ============================================================
# 🎤 tone_engine.py — Core4.AI Engine Layer 1
# ------------------------------------------------------------
# Purpose:
#   - Define brand tone profiles
#   - Used later by narrative_engine & copilot_engine
# ============================================================

from typing import Dict


class ToneEngine:
    def __init__(self):
        self.tones = {
            "bold": {
                "style": "Direct, confident, energetic",
                "keywords": ["power", "lead", "dominate", "take control"]
            },
            "friendly": {
                "style": "Warm, helpful, positive",
                "keywords": ["discover", "enjoy", "smile", "experience"]
            },
            "luxury": {
                "style": "Elegant, premium, calm",
                "keywords": ["crafted", "exclusive", "refined", "signature"]
            },
            "tech": {
                "style": "Smart, precise, modern",
                "keywords": ["optimized", "engineered", "advanced", "performance"]
            }
        }

    def get_tone(self, tone: str) -> Dict:
        return self.tones.get(tone, self.tones["friendly"])
