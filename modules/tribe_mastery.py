# ============================================================
# 💎 Core4.AI – Tribe Mastery Router
# Handles: auto-assignment to tribes by average mastery
# ============================================================

from fastapi import APIRouter
from pydantic import BaseModel
import random

router = APIRouter()

# --- Models ---
class TribeAssignment(BaseModel):
    creator_id: int
    tribe_id: int
    tribe_name: str
    avg_mastery: float
    reason: str


tribe_names = ["Vibe Makers", "Deep Thinkers", "Humor League", "Trend Alchemists"]


# --- POST /tribe/reassign ---
@router.post("/reassign", response_model=TribeAssignment)
async def reassign_creator(creator_id: int, score: float):
    # Simulated logic: assign to tribe with similar average mastery (±5)
    avg_mastery = score + random.uniform(-5, 5)
    tribe_id = random.randint(1, len(tribe_names))
    tribe_name = tribe_names[tribe_id - 1]

    return TribeAssignment(
        creator_id=creator_id,
        tribe_id=tribe_id,
        tribe_name=tribe_name,
        avg_mastery=round(avg_mastery, 2),
        reason=f"Matched to tribe with average mastery ±5 → {tribe_name}",
    )
