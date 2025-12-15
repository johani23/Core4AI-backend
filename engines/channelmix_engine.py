# ============================================================
# 📡 channelmix_engine.py — Core4.AI Layer 3
# ------------------------------------------------------------
# Purpose:
#   Recommend distribution mix across platforms
# ============================================================

class ChannelMixEngine:
    def __init__(self):
        self.defaults = {
            "tiktok": 0.4,
            "instagram": 0.3,
            "snapchat": 0.2,
            "youtube": 0.1
        }

    def recommend(self, persona: str, fit_score: float):
        mix = self.defaults.copy()

        if persona == "Techy":
            mix["youtube"] += 0.1
            mix["snapchat"] -= 0.1

        if fit_score > 0.8:
            mix["tiktok"] += 0.1

        # normalize
        total = sum(mix.values())
        for k in mix:
            mix[k] = round(mix[k] / total, 3)

        return mix
