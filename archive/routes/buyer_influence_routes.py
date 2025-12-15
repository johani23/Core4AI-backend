# ============================================================
# 💚 Core4.AI – Buyer Influence Engine (v2.0 FINAL)
# ============================================================

from fastapi import APIRouter
from routes.buyer_profile_routes import BUYERS

router = APIRouter(prefix="/api/buyer/influence", tags=["Buyer Influence"])


# ------------------------------------------------------------
# CALCULATE INFLUENCE SCORE
# ------------------------------------------------------------
def calculate_influence_score(buyer_id: str):
    b = BUYERS.get(buyer_id)
    if not b:
        return 0

    score = 0
    score += b["tokens"] * 0.15          # 15% weight of tokens
    score += b["referral_success"] * 12   # strong weight for referrals
    score += b["r_and_d_score"] * 3       # R&D contributes
    score += len(b["tested_products"]) * 2  # product experience

    return round(score, 2)


# ------------------------------------------------------------
# DETERMINE TIER
# ------------------------------------------------------------
def determine_influence_tier(buyer_id: str):
    score = calculate_influence_score(buyer_id)

    if score >= 25:
        return "Influencer"
    elif score >= 10:
        return "Rising Influencer"
    elif score >= 3:
        return "Active Buyer"
    else:
        return "Newbie"


# ------------------------------------------------------------
# PUBLIC API – INFLUENCE STATUS (used by BuyerUpgrade.jsx)
# ------------------------------------------------------------
@router.get("/status/{buyer_id}")
def get_influence_status(buyer_id: str):

    if buyer_id not in BUYERS:
        return {"error": "Buyer not found"}

    tier = determine_influence_tier(buyer_id)
    score = calculate_influence_score(buyer_id)
    b = BUYERS[buyer_id]

    return {
        "buyer_id": buyer_id,
        "tier": tier,
        "influence_score": score,
        "r_and_d_score": b["r_and_d_score"],
        "referral_success": b["referral_success"],
        "influencer_ready": b["influencer_ready"],
        "tested_products": len(b["tested_products"]),
    }


# ------------------------------------------------------------
# PUBLIC API – RAW SCORE ONLY (optional for analytics)
# ------------------------------------------------------------
@router.get("/score/{buyer_id}")
def get_influence_score(buyer_id: str):
    return {"buyer_id": buyer_id, "score": calculate_influence_score(buyer_id)}


# ------------------------------------------------------------
# PUBLIC API – TIER ONLY
# ------------------------------------------------------------
@router.get("/tier/{buyer_id}")
def get_influence_tier(buyer_id: str):
    return {
        "buyer_id": buyer_id,
        "tier": determine_influence_tier(buyer_id),
        "score": calculate_influence_score(buyer_id),
    }
