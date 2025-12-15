from fastapi import APIRouter

router = APIRouter(
    prefix="/api/merchant/analytics",
    tags=["merchant-analytics"]
)

@router.get("/overview")
async def overview():
    return {
        "sales": 12400,
        "orders": 83,
        "visitors": 1248,
        "sales_growth": 18,
        "engagement": 14,
        "top_products": [
            {"name": "Smart Kettle X1", "growth": 18},
            {"name": "Wireless Earbuds Pro", "growth": 12},
            {"name": "Backpack Pro", "growth": 9},
        ]
    }
