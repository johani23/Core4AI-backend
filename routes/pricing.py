# ============================================================================
# 💸 Core4AI – Pricing Engine API (Feature × Audience)
# ============================================================================

from fastapi import APIRouter
from pydantic import BaseModel
from engines.pricing.pricing_engine import compute_best_price

router = APIRouter(
    prefix="/api/pricing",
    tags=["pricing"]
)

class PricingInput(BaseModel):
    product: dict
    rnd: dict | None = None

@router.post("/compute")
async def compute_price(data: PricingInput):
    result = compute_best_price(data.product, data.rnd)
    return {"status": "success", "pricing": result}
