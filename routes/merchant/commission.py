# ============================================================================
# 💚 Core4AI – Merchant Commission API (v1)
# ============================================================================

from fastapi import APIRouter
from pydantic import BaseModel
from engines.commission.commission_engine import (
    calculate_commission,
    estimate_merchant_profit,
    generate_commission_breakdown
)

router = APIRouter(
    prefix="/api/merchant/commission",
    tags=["merchant-commission"]
)

class CommissionInput(BaseModel):
    price: float
    commission_rate: float
    conversions: int
    cost: float = 0

@router.post("/calculate")
async def commission_calculation(data: CommissionInput):
    earnings = calculate_commission(
        price=data.price,
        commission_rate=data.commission_rate,
        conversions=data.conversions
    )
    breakdown = generate_commission_breakdown(
        price=data.price,
        commission_rate=data.commission_rate,
        conversions=data.conversions
    )
    return {"status": "success", "total_commission": earnings, "breakdown": breakdown}

@router.post("/profit")
async def merchant_profit(data: CommissionInput):
    profit = estimate_merchant_profit(
        price=data.price,
        cost=data.cost,
        conversions=data.conversions,
        commission_rate=data.commission_rate
    )
    return {"status": "success", "merchant_profit": profit}

@router.get("/example")
async def example():
    price = 100
    commission_rate = 0.10
    conversions = 5
    cost = 30
    return {
        "commission": calculate_commission(price, commission_rate, conversions),
        "profit": estimate_merchant_profit(price, cost, conversions, commission_rate),
        "breakdown": generate_commission_breakdown(price, commission_rate, conversions)
    }
