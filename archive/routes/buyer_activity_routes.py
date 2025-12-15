# ============================================================
# 💚 buyer_activity_routes.py — Raw Activity Log (FINAL)
# ============================================================

from fastapi import APIRouter
from routes.buyer_profile_routes import BUYERS

router = APIRouter(prefix="/api/buyer/activity", tags=["Buyer Activity"])


@router.get("/{buyer_id}")
def activity(buyer_id: str):
    if buyer_id not in BUYERS:
        return {"error": "Buyer not found"}

    return {
        "buyer_id": buyer_id,
        "events": BUYERS[buyer_id]["events"]
    }
