# ============================================================
# 💚 Core4.AI – Auto Creator Creation (v1.0)
# ------------------------------------------------------------
# Automatically creates a Creator profile when a Buyer becomes Influencer
# ============================================================

from fastapi import APIRouter
from routes.buyer_profile_routes import BUYERS
from routes.buyer_influence_routes import determine_influence_tier

router = APIRouter(prefix="/api/creator/auto", tags=["Creator-Auto"])

# Local in-memory creator DB
CREATORS = {}


# ------------------------------------------------------------
# ✔ Auto-create Creator Profile from Buyer
# ------------------------------------------------------------
def create_creator_from_buyer(buyer_id: str):
    b = BUYERS.get(buyer_id)
    if not b:
        return None

    CREATORS[buyer_id] = {
        "creator_id": buyer_id,
        "name": b["name"],
        "niche": b.get("tribe_fit", "General"),
        "joined_at": "auto",
        "total_posts": 0,
        "creator_score": 0,
        "followers": 0,
        "bio": f"Started as a buyer, now a rising creator on Core4.AI ✨"
    }

    # Mark buyer as Creator
    b["is_creator"] = True

    return CREATORS[buyer_id]


# ------------------------------------------------------------
# 🔥 Public API (Manual trigger for testing)
# ------------------------------------------------------------
@router.post("/convert/{buyer_id}")
def convert(buyer_id: str):
    tier = determine_influence_tier(buyer_id)

    if tier != "Influencer":
        return {"status": "not_ready", "tier": tier}

    new_creator = create_creator_from_buyer(buyer_id)
    return {"status": "created", "creator": new_creator}
