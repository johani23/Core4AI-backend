# ============================================================
# 💚 buyer_rnd_routes.py — R&D / Willingness-to-Pay Engine
# ============================================================

from fastapi import APIRouter
from pydantic import BaseModel
from routes.buyer_profile_routes import BUYERS, log_event

router = APIRouter(prefix="/api/buyer/rnd", tags=["Buyer R&D"])

class RNDInput(BaseModel):
    value: float
    feedback: str = ""

@router.post("/submit/{buyer_id}")
def submit_rnd(buyer_id: str, data: RNDInput):

    if buyer_id not in BUYERS:
        return {"error": "Buyer not found"}

    # Update R&D score
    BUYERS[buyer_id]["r_and_d_score"] += data.value

    # Log event
    log_event(
        buyer_id,
        "R&D Submitted",
        f"WTP +{data.value}. Feedback: {data.feedback}",
        "🧠"
    )

    # Reward tokens
    BUYERS[buyer_id]["tokens"] += 2

    return {
        "status": "ok",
        "r_and_d_score": BUYERS[buyer_id]["r_and_d_score"],
        "tokens": BUYERS[buyer_id]["tokens"]
    }
