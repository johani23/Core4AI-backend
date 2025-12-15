# ============================================================
# 💚 Core4.AI – Creator XP Engine (v1.0 FINAL)
# ------------------------------------------------------------
# Handles:
# • XP Gain
# • Level Progression
# • XP Tiers
# • Influence Boost
# • XP Events Log
# ============================================================

from fastapi import APIRouter
from pydantic import BaseModel
import datetime

# Import creator store
from routes.creator_profile_routes import CREATORS, log_creator_event

router = APIRouter(prefix="/api/creator/xp", tags=["Creator XP"])


# ------------------------------------------------------------
# XP → Level Mapping
# ------------------------------------------------------------
XP_LEVELS = {
    1: 0,
    2: 100,
    3: 250,
    4: 600,
    5: 1200,
}

def calculate_level(xp: int):
    """Returns the level based on XP."""
    current_level = 1
    for lvl, req in XP_LEVELS.items():
        if xp >= req:
            current_level = lvl
    return current_level


# ------------------------------------------------------------
# XP Gain Model
# ------------------------------------------------------------
class XPGain(BaseModel):
    creator_id: str
    action: str
    xp_amount: int


# ------------------------------------------------------------
# Award XP
# ------------------------------------------------------------
@router.post("/gain")
def xp_gain(data: XPGain):

    cid = data.creator_id

    if cid not in CREATORS:
        return {"error": "Creator not found"}

    creator = CREATORS[cid]

    # add XP
    creator["xp"] += data.xp_amount

    # recalc level
    new_level = calculate_level(creator["xp"])
    level_up = new_level > creator["level"]
    creator["level"] = new_level

    # influence score boost (XP makes creator stronger)
    creator["influence_score"] = round(creator["xp"] * 0.12, 2)

    # log event
    log_creator_event(
        cid,
        "XP Gained",
        f"Action '{data.action}' → +{data.xp_amount} XP",
        "✨"
    )

    if level_up:
        log_creator_event(
            cid,
            "Level Up",
            f"Congratulations! Upgraded to Level {new_level}",
            "🚀"
        )

    return {
        "status": "xp_added",
        "creator_id": cid,
        "new_xp": creator["xp"],
        "level": creator["level"],
        "influence_score": creator["influence_score"],
        "level_up": level_up
    }


# ------------------------------------------------------------
# Public: Get XP + Level Stats
# ------------------------------------------------------------
@router.get("/status/{creator_id}")
def get_xp_status(creator_id: str):

    if creator_id not in CREATORS:
        return {"error": "Creator not found"}

    c = CREATORS[creator_id]
    next_level_req = None

    # compute next level requirement
    for lvl, req in XP_LEVELS.items():
        if req > c["xp"]:
            next_level_req = req - c["xp"]
            break

    return {
        "creator_id": creator_id,
        "xp": c["xp"],
        "level": c["level"],
        "influence_score": c["influence_score"],
        "xp_to_next_level": next_level_req
    }
