# ============================================================
# 💚 Core4.AI – Creator Earnings Engine (v1.0 FINAL)
# ------------------------------------------------------------
# Tracks:
#   • Earnings from conversions
#   • Earnings from tribe splits
#   • Earnings from merchant deals
#   • Total & monthly earnings
#   • Events logging to Creator Timeline
# ============================================================

from fastapi import APIRouter
from pydantic import BaseModel
import datetime

from routes.creator_profile_routes import CREATORS, log_creator_event

router = APIRouter(prefix="/api/creator/earnings", tags=["Creator Earnings"])


# ------------------------------------------------------------
# Internal In-Memory Store
# ------------------------------------------------------------
EARNINGS = {}  # {creator_id: [ { amount, source, timestamp } ]}


# ------------------------------------------------------------
# Earnings Model
# ------------------------------------------------------------
class EarningEvent(BaseModel):
    creator_id: str
    amount: float
    source: str  # "conversion", "tribe_split", "deal", etc.


# ------------------------------------------------------------
# Register Creator Earnings Structure
# ------------------------------------------------------------
def ensure_creator_store(cid):
    if cid not in EARNINGS:
        EARNINGS[cid] = []


# ------------------------------------------------------------
# Add Earnings to Creator
# ------------------------------------------------------------
@router.post("/add")
def add_earnings(data: EarningEvent):

    cid = data.creator_id

    if cid not in CREATORS:
        return {"error": "Creator not found"}

    ensure_creator_store(cid)

    event = {
        "amount": round(data.amount, 2),
        "source": data.source,
        "timestamp": datetime.datetime.now().isoformat()
    }

    EARNINGS[cid].append(event)

    # update creator wallet
    CREATORS[cid]["earnings"] += data.amount

    # log creator timeline event
    log_creator_event(
        cid,
        "Earnings Added",
        f"+{data.amount:.2f} SAR from {data.source}",
        "💵"
    )

    return {"status": "added", "creator_id": cid, "earnings": CREATORS[cid]["earnings"]}


# ------------------------------------------------------------
# Get Earnings Summary
# ------------------------------------------------------------
@router.get("/summary/{creator_id}")
def get_earnings_summary(creator_id: str):

    if creator_id not in CREATORS:
        return {"error": "Creator not found"}

    ensure_creator_store(creator_id)

    total = round(sum(e["amount"] for e in EARNINGS[creator_id]), 2)

    # last 30 days
    now = datetime.datetime.now()
    monthly_total = round(sum(
        e["amount"]
        for e in EARNINGS[creator_id]
        if (now - datetime.datetime.fromisoformat(e["timestamp"])).days <= 30
    ), 2)

    return {
        "creator_id": creator_id,
        "total_earnings": total,
        "monthly_earnings": monthly_total,
        "events": EARNINGS[creator_id][-10:],  # last 10 events
    }


# ------------------------------------------------------------
# Last Earnings Events (for UI)
# ------------------------------------------------------------
@router.get("/events/{creator_id}")
def last_earnings_events(creator_id: str):

    if creator_id not in CREATORS:
        return {"error": "Creator not found"}

    ensure_creator_store(creator_id)

    return {
        "creator_id": creator_id,
        "events": list(reversed(EARNINGS[creator_id][-10:]))
    }
