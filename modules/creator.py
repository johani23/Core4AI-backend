# ============================================================
# 💎 Core4.AI – Creator Router  (MVP-77 + Auto-Tribe Assignment)
# Handles: content uploads, AI scoring, level retrieval
# ============================================================

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
import random, httpx

router = APIRouter()

# --- Data model for score response ---
class MasteryResult(BaseModel):
    creator_id: int
    score: float
    level_name: str
    tribe: str | None = None


# --- Helper: determine mastery tier ---
def get_mastery_label(score: float) -> str:
    if score < 40:
        return "🌱 Rising Voice"
    elif score < 65:
        return "🔥 Emerging"
    elif score < 85:
        return "💎 Core Creator"
    else:
        return "🧠 Mentor"


# --- POST /creator/analyze ---
@router.post("/analyze", response_model=MasteryResult)
async def analyze_clip(creator_id: int = Form(...), file: UploadFile = File(...)):
    # ⚙️ Mock AI scoring (0–100). Replace with real model later.
    score = round(random.uniform(25, 95), 2)
    level = get_mastery_label(score)

    # ⚡ Auto-assign tribe by calling Tribe Mastery router
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                "http://127.0.0.1:8000/tribe/reassign",
                params={"creator_id": creator_id, "score": score},
                timeout=10.0,
            )
            tribe_data = resp.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Tribe assignment failed: {e}")

    return MasteryResult(
        creator_id=creator_id,
        score=score,
        level_name=level,
        tribe=tribe_data.get("tribe_name"),
    )


# --- GET /creator/level/{creator_id} ---
@router.get("/level/{creator_id}", response_model=MasteryResult)
async def get_creator_level(creator_id: int):
    # Example static lookup; in production query DB.
    score = round(random.uniform(25, 95), 2)
    level = get_mastery_label(score)

    # call tribe reassign for consistency
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "http://127.0.0.1:8000/tribe/reassign",
            params={"creator_id": creator_id, "score": score},
        )
        tribe_data = resp.json()

    return MasteryResult(
        creator_id=creator_id,
        score=score,
        level_name=level,
        tribe=tribe_data.get("tribe_name"),
    )
