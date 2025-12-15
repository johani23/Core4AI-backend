# ============================================================================
# 💚 Core4AI – Merchant Influencers API (v1)
# ============================================================================

from fastapi import APIRouter

router = APIRouter(
    prefix="/api/merchant/influencers",
    tags=["merchant-influencers"]
)

dummy_influencers = [
    {"id": 1, "name": "ناصر", "followers": "350K", "category": "لايف ستايل", "price": 950, "expectedSales": 8},
    {"id": 2, "name": "دانه", "followers": "220K", "category": "جمال", "price": 750, "expectedSales": 5},
    {"id": 3, "name": "عبدالله", "followers": "400K", "category": "مراجعات", "price": 1200, "expectedSales": 10},
    {"id": 4, "name": "منى", "followers": "180K", "category": "طبخ", "price": 680, "expectedSales": 6},
]

@router.get("/list")
async def list_influencers():
    return {
        "status": "success",
        "influencers": dummy_influencers
    }

@router.get("/test")
async def test():
    return {"status": "ok", "endpoint": "merchant.influencers"}
