# ============================================================
# 🤖 copilot_engine.py — Core4.AI Layer 3
# ------------------------------------------------------------
# Purpose:
#   Suggest improvements, rewrites, and tone adjustments
# ============================================================

class CoPilotEngine:
    def __init__(self, tone_engine):
        self.tone_engine = tone_engine

    def rewrite(self, text: str, tone: str):
        tone_profile = self.tone_engine.get_tone(tone)
        style = tone_profile["style"]

        return f"[{style}] {text}"

    def strengthen_message(self, text: str):
        return text.replace("good", "exceptional").replace("nice", "powerful")

    def shorten(self, text: str):
        if len(text) <= 90:
            return text
        return text[:87] + "..."
