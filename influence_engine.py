# ============================================================================
# 💚 Core4.AI – Influence Engine v1.0 (Score + Tiers)
# ============================================================================

import math
from typing import List, Dict

# -----------------------------
# Base event weights
# -----------------------------
WEIGHTS = {
    "view": 1,
    "long_view": 5,
    "click": 6,
    "save": 10,
    "share": 20,
    "purchase": 30,
    "return_session": 20,
    "tribe_switch": 8,
}

# -----------------------------
# Mood multipliers
# -----------------------------
MOOD_MULTIPLIER = {
    "مرتاح": 1.0,
    "متحمس": 1.3,
    "فضولي": 1.1,
    "مشتت": 0.9,
}

# ---------------------------------------------------------
# Influence Score Calculation
# ---------------------------------------------------------
def compute_influence(events: List[Dict], persona: Dict):
    base = 0

    for e in events:
        event = e["event_type"]
        base += WEIGHTS.get(event, 0)

    # mood effect
    mood = persona.get("mood", "مرتاح")
    base *= MOOD_MULTIPLIER.get(mood, 1.0)

    # Non-linear scaling (soft exponential)
    score = math.log1p(base) * 25

    return round(score)

# ---------------------------------------------------------
# Influence Tiers
# ---------------------------------------------------------
def get_influence_tier(score: int) -> str:
    if score < 30:
        return "Explorer"
    if score < 75:
        return "Rising Micro-Influencer"
    if score < 130:
        return "Mid Influencer"
    if score < 200:
        return "Top Influencer"
    return "Power Influencer"
