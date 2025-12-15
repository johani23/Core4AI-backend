# ============================================================
# ✍️ autodraft_engine.py — Core4.AI Layer 3
# ------------------------------------------------------------
# Purpose:
#   Auto-generate draft captions, ad copies, and content ideas
# ============================================================

class AutoDraftEngine:
    def __init__(self, narrative_engine):
        self.narrative_engine = narrative_engine

    def draft_caption(self, narrative: dict):
        return f"{narrative['hook']} — {narrative['narrative']}"

    def draft_ad_copy(self, narrative: dict):
        return (
            f"✨ {narrative['hook']}\n"
            f"{narrative['narrative']}\n"
            f"Tap to discover more."
        )

    def draft_variations(self, narrative: dict):
        base = narrative["narrative"]
        return [
            f"{narrative['hook']} | {base}",
            f"Experience the difference — {base}",
            f"Why settle for less? {base}"
        ]
