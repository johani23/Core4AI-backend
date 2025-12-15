# ============================================================================
# 💚 Core4AI – Merchant Pricing API (MVP Stable Edition)
# ============================================================================

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/api/merchant/pricing",
    tags=["merchant-pricing"]
)

# -----------------------------------------------------------------------
# Dummy Pricing Algorithms (Safe, Stable, No Legacy Imports)
# -----------------------------------------------------------------------

def calculate_evc(product_price, competitor_price, feature_value):
    """
    Simple EVC (Economic Value to Customer)
    """
    base_value = competitor_price + feature_value
    recommended = (base_value + product_price) / 2
    return round(recommended, 2)


def calculate_elasticity(product_price, competitor_price):
    """
    Simple elasticity indicator
    """
    diff = product_price - competitor_price
    if diff <= 10:
        return 0.5      # low sensitivity
    elif diff <= 30:
        return 1.0      # medium
    else:
        return 1.5      # high sensitivity


def generate_reaction(elasticity):
    if elasticity < 0.7:
        return "ممتاز – السعر مقبول جداً"
    elif elasticity < 1.2:
        return "جيد – يحتاج محتوى قوي"
    else:
        return "حساس – نوصّي بتعديل بسيط"


def calculate_range(best_price):
    return f"{best_price - 10} – {best_price + 10}"


# -----------------------------------------------------------------------
# Input Model
# -----------------------------------------------------------------------

class PricingInput(BaseModel):
    product_price: float
    competitor_price: float
    feature_value: float


# -----------------------------------------------------------------------
# Main Endpoint
# -----------------------------------------------------------------------

@router.post("/calculate")
async def calculate_price(data: PricingInput):

    best_price = calculate_evc(
        data.product_price,
        data.competitor_price,
        data.feature_value
    )

    elasticity = calculate_elasticity(
        data.product_price,
        data.competitor_price
    )

    reaction = generate_reaction(elasticity)

    return {
        "status": "success",
        "best_price": best_price,
        "range": calculate_range(best_price),
        "elasticity": elasticity,
        "reaction": reaction
    }
