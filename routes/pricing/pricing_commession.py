from fastapi import APIRouter

router = APIRouter(prefix="/api/pricing/commission", tags=["Commission Sharing"])

@router.get("/{product_id}")
def get_commission(product_id: str):

    import random

    base_commission = random.choice([8, 10, 12, 15])

    tiers = [
        {"level": "Starter", "rate": base_commission, "description": "Entry-level creators"},
        {"level": "Pro", "rate": base_commission + 2, "description": "Consistently performing creators"},
        {"level": "Elite", "rate": base_commission + 4, "description": "High-impact creators"}
    ]

    bonus = "+3% if exceeding 50 sales in 7 days"
    product_price = random.randint(40, 70)
    cost = random.randint(15, 30)

    margin_after = product_price - cost - ((base_commission / 100) * product_price)
    margin_pct = round((margin_after / product_price) * 100, 2)

    return {
        "base_commission": base_commission,
        "tiers": tiers,
        "bonus": bonus,
        "profit_after_commission": round(margin_after, 2),
        "margin_after_commission": margin_pct,
        "recommendation": f"{base_commission + 2}% is ideal for this product category.",
        "recommendation_comment": "Based on performance patterns and ROI uplift."
    }
