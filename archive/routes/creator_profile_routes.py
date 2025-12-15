# ============================================================
# 💚 Core4.AI – Creator Profile Engine (v1.0 FINAL)
# ------------------------------------------------------------
# This file controls:
# • Creator Profile
# • Creator Level
# • Creator XP
# • Creator Earnings
# • Creator Events
# • Buyer → Creator Auto-Creation
# ============================================================

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
import datetime

# -----------------------------------------
# SHARED BUYER STORE (IMPORT BUYERS)
# -----------------------------------------
from routes.buyer_profile_routes import BUYERS

router = APIRouter(prefix="/api/creator", tags=["Creator"])

# -----------------------------------------
# INTERNAL CREATOR STORE
# -----------------------------------------
CREATORS = {}


# ------------------------------------------------------------
# Creator Profile Model
# ------------------------------------------------------------
class CreatorProfile(BaseModel):
    creator_id: str
    name: str
    xp: int = 0
    level: int = 1
    earning_balance: float = 0.0
    promoted_products: List[str] = []
    content_history: List[dict] = []
    influence_score: float = 0.0
    tier: str = "New Creator"  # Bronze / Silver / Gold / Elite
    events: List[dict] = []


# ------------------------------------------------------------
# EVENT LOGGER
# ------------------------------------------------------------
def log_creator_event(cid: str, type: str, description: str, icon="⚡"):
    if cid not in CREATORS:
        return

    CREATORS[cid]["events"].append({
        "type": type,
        "description": description,
        "icon": icon,
        "timestamp": datetime.datetime.now().isoformat()
    })


# ------------------------------------------------------------
# AUTO-CREATE CREATOR WHEN BUYER UPGRADES
# ------------------------------------------------------------
def auto_create_creator(buyer_id: str):

    if buyer_id not in BUYERS:
        return None

    if buyer_id in CREATORS:
        return CREATORS[buyer_id]

    b = BUYERS[buyer_id]

    profile = {
        "creator_id": buyer_id,
        "name": b["name"],
        "xp": 0,
        "level": 1,
        "earning_balance": 0.0,
        "promoted_products": [],
        "content_history": [],
        "influence_score": 0.0,
        "tier": "New Creator",
        "events": []
    }

    CREATORS[buyer_id] = profile

    log_creator_event(buyer_id, "Creator Activated", "Buyer has become a creator!", "🔥")

    return profile


# ------------------------------------------------------------
# PUBLIC: Get Creator Profile
# ------------------------------------------------------------
@router.get("/{creator_id}")
def get_creator(creator_id: str):

    if creator_id not in CREATORS:
        return {"error": "Creator not found"}

    return CREATORS[creator_id]


# ------------------------------------------------------------
# PUBLIC: Initialize Creator Manually (optional)
# ------------------------------------------------------------
@router.post("/create/{buyer_id}")
def manual_create_creator(buyer_id: str):

    profile = auto_create_creator(buyer_id)

    if profile is None:
        return {"error": "Buyer does not exist"}

    return {"status": "created", "creator": profile}


# ------------------------------------------------------------
# PUBLIC: Add XP
# ------------------------------------------------------------
@router.post("/{creator_id}/xp/{amount}")
def add_xp(creator_id: str, amount: int):

    if creator_id not in CREATORS:
        return {"error": "Creator not found"}

    CREATORS[creator_id]["xp"] += amount

    log_creator_event(creator_id, "XP Earned", f"+{amount} XP", "✨")

    return CREATORS[creator_id]


# ------------------------------------------------------------
# PUBLIC: Add Earnings
# ------------------------------------------------------------
@router.post("/{creator_id}/earn/{amount}")
def add_earnings(creator_id: str, amount: float):

    if creator_id not in CREATORS:
        return {"error": "Creator not found"}

    CREATORS[creator_id]["earning_balance"] += amount

    log_creator_event(creator_id, "Earnings Added", f"+{amount} SAR", "💰")

    return CREATORS[creator_id]
