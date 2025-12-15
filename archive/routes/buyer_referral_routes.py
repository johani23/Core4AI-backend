# ============================================================
# 💚 buyer_referral_routes.py — Referral Engine (v2.0 FINAL)
# ============================================================

from fastapi import APIRouter
from routes.buyer_profile_routes import BUYERS, log_event

router = APIRouter(prefix="/api/buyer/referral", tags=["Buyer Referral"])

# ------------------------------------------------------------
# ADD REFERRAL SUCCESS
# ------------------------------------------------------------
@router.post("/{buyer_id}")
def add_referral(buyer_id: str):

    if buyer_id not in BUYERS:
        return {"error": "Buyer not found"}

    BUYERS[buyer_id]["referral_success"] += 1
    BUYERS[buyer_id]["tokens"] += 5   # reward tokens

    # Log event into timeline
    log_event(
        buyer_id,
        "Referral Success",
        "A successful referral was recorded.",
        "🎯"
    )

    return {
        "status": "ok",
        "referral_success": BUYERS[buyer_id]["referral_success"],
        "tokens": BUYERS[buyer_id]["tokens"]
    }
