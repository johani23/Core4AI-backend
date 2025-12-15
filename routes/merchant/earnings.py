# ============================================================================
# 💚 Core4AI – Merchant Earnings API (MVP dummy, no merchant_id)
# ============================================================================

from fastapi import APIRouter

router = APIRouter(
    prefix="/api/merchant/earnings",
    tags=["merchant-earnings"]
)

@router.get("/")
async def get_earnings():
    return {
        "status": "success",
        "today": 1200,
        "week": 5400,
        "month": 15800,
        "influencers": [
            {"name": "ناصر", "sales": 8, "payout": 120},
            {"name": "دانه", "sales": 3, "payout": 75},
            {"name": "عبدالله", "sales": 5, "payout": 95}
        ]
    }

@router.get("/test")
async def test():
    return {"ok": True, "endpoint": "merchant.earnings"}
