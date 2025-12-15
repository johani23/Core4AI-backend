# ============================================================
# 💎 Core4.AI – Feedback Engine Router
# Handles: personalized tips + next challenge suggestions
# ============================================================

from fastapi import APIRouter
from pydantic import BaseModel
import random

router = APIRouter()

class FeedbackReport(BaseModel):
    creator_id: int
    score: float
    level_name: str
    tips: list[str]
    next_challenge: str

TIPS_POOL = {
    "Rising Voice": [
        "Focus on clear audio & lighting.",
        "Post 2-3 times weekly to build rhythm.",
    ],
    "Emerging": [
        "Add emotional hooks in first 5 seconds.",
        "Collaborate with peers for reach.",
    ],
    "Core Creator": [
        "Refine storytelling and visual branding.",
        "Experiment with new challenge formats.",
    ],
    "Mentor": [
        "Host mini-workshops or mentorship duels.",
        "Create content about your creative process.",
    ],
}

@router.get("/{creator_id}", response_model=FeedbackReport)
async def get_feedback(creator_id: int):
    score = round(random.uniform(25, 95), 2)

    if score < 40:
        level = "Rising Voice"
    elif score < 65:
        level = "Emerging"
    elif score < 85:
        level = "Core Creator"
    else:
        level = "Mentor"

    tips = random.sample(TIPS_POOL[level], k=2)
    next_challenge = f"Upload a {level.lower()}-level clip with new theme intensity!"

    return FeedbackReport(
        creator_id=creator_id,
        score=score,
        level_name=level,
        tips=tips,
        next_challenge=next_challenge,
    )
