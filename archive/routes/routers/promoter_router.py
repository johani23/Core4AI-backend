from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

PROMOTER_EARNINGS = {}
CREATOR_EARNINGS = {}
SUBTRIBE_EARNINGS = {}

# -------------------------------
# 1) Click Registration
# -------------------------------
@router.post("/register-click")
def register_click(data: dict):
    user_id = data["user_id"]
    product_id = data["product_id"]
    creator_id = data["creator_id"]
    timestamp = datetime.utcnow()

    return {
        "status": "click_registered",
        "user_id": user_id,
        "product_id": product_id,
        "creator_id": creator_id,
        "timestamp": timestamp
    }

# -------------------------------
# 2) Sale Event
# -------------------------------
@router.post("/sale")
def sale_event(data: dict):

    amount = data["amount"]
    promoter_id = data["promoter_id"]
    creator_id = data["creator_id"]
    tribe_id = data.get("tribe_id", None)
    subtribe_id = data.get("subtribe_id", None)

    # Commission Split %
    creator_cut = amount * 0.35
    promoter_cut = amount * 0.50
    subtribe_cut = amount * 0.15 if subtribe_id else 0

    # Save earnings
    CREATOR_EARNINGS[creator_id] = CREATOR_EARNINGS.get(creator_id, 0) + creator_cut
    PROMOTER_EARNINGS[promoter_id] = PROMOTER_EARNINGS.get(promoter_id, 0) + promoter_cut

    if subtribe_id:
        SUBTRIBE_EARNINGS[subtribe_id] = SUBTRIBE_EARNINGS.get(subtribe_id, 0) + subtribe_cut

    return {
        "status": "sale_recorded",
        "amount": amount,
        "creator": creator_cut,
        "promoter": promoter_cut,
        "subtribe": subtribe_cut
    }

# -------------------------------
# 3) Cancel Sale
# -------------------------------
@router.post("/cancel-sale")
def cancel_sale(data: dict):

    promoter_id = data["promoter_id"]
    creator_id = data["creator_id"]
    amount = data["amount"]
    subtribe_id = data.get("subtribe_id", None)

    # Commission Split %
    creator_cut = amount * 0.35
    promoter_cut = amount * 0.50
    subtribe_cut = amount * 0.15 if subtribe_id else 0

    CREATOR_EARNINGS[creator_id] -= creator_cut
    PROMOTER_EARNINGS[promoter_id] -= promoter_cut

    if subtribe_id:
        SUBTRIBE_EARNINGS[subtribe_id] -= subtribe_cut

    return {"status": "sale_reversed"}
