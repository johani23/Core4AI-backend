# ============================================================
# 💚 Core4.AI – Influencer Transition Engine (v2.0 AUTO-CREATOR)
# ============================================================

from fastapi import APIRouter
from routes.buyer_profile_routes import BUYERS
from routes.buyer_influence_routes import calculate_influence_score, determine_influence_tier

# ✨ NEW — Creator Registry
CREATORS = {}

router = APIRouter(prefix="/api/buyer/transition", tags=["Influencer Transition"])

# ------------------------------------------------------------
# RULES TO BECOME INFLUENCER
# ------------------------------------------------------------
MIN_SCORE = 25
MIN_REFERRALS = 1
MIN_RND = 2
MIN_TESTED = 1

def is_eligible(b):
    return (
        calculate_influence_score(b["buyer_id"]) >= MIN_SCORE and
        b["referral_success"] >= MIN_REFERRALS and
        b["r_and_d_score"] >= MIN_RND and
        len(b["tested_products"]) >= MIN_TESTED
    )

# ------------------------------------------------------------
# AUTO-CREATE CREATOR PROFILE
# ------------------------------------------------------------
def auto_create_creator(buyer_id: str):
    """Generate a Creator Profile when user becomes Influencer"""
    CREATORS[buyer_id] = {
        "creator_id": buyer_id,
        "bio": "New creator powered by Core4.AI!",
        "content_count": 0,
        "followers": 0,
        "earning_rate": 0.0,
        "category": None,
        "joined_at": None,
        "is_active": True
    }
    return CREATORS[buyer_id]

# ------------------------------------------------------------
# CHECK TRANSITION STATUS
# ------------------------------------------------------------
@router.get("/status/{buyer_id}")
def check_transition(buyer_id: str):

    if buyer_id not in BUYERS:
        return {"error": "Buyer not found"}

    b = BUYERS[buyer_id]

    score = calculate_influence_score(buyer_id)
    tier = determine_influence_tier(buyer_id)

    return {
        "buyer_id": buyer_id,
        "tier": tier,
        "score": score,
        "eligible": is_eligible(b),
        "requirements": {
            "min_score": MIN_SCORE,
            "min_referrals": MIN_REFERRALS,
            "min_rnd": MIN_RND,
            "min_tested_products": MIN_TESTED
        }
    }

# ------------------------------------------------------------
# EXECUTE TRANSITION (WITH AUTO-CREATOR CREATION)
# ------------------------------------------------------------
@router.post("/upgrade/{buyer_id}")
def upgrade_to_influencer(buyer_id: str):

    if buyer_id not in BUYERS:
        return {"error": "Buyer not found"}

    b = BUYERS[buyer_id]

    if not is_eligible(b):
        return {
            "status": "not_ready",
            "reason": "Buyer does not meet all upgrade requirements",
            "data": check_transition(buyer_id)
        }

    # Mark as influencer
    b["influencer_ready"] = True

    # ✨ AUTO-CREATE CREATOR PROFILE
    creator_profile = auto_create_creator(buyer_id)

    return {
        "status": "success",
        "message": "Buyer upgraded to Influencer 🎉 Creator profile generated.",
        "tier": "Influencer",
        "buyer": b,
        "creator_profile": creator_profile
    }
