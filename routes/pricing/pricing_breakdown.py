from fastapi import APIRouter, Request

router = APIRouter(prefix="/api/pricing/breakdown", tags=["Pricing Breakdown"])

@router.get("/{product_id}")
def breakdown_api(product_id: str, request: Request):

    PRODUCTS = request.app.state.products
    pricing_engine = request.app.state.pricing_engine

    product = None
    for _, plist in PRODUCTS.items():
        for p in plist:
            if p["product_id"] == product_id:
                product = p
                break

    if not product:
        return {"error": "Product not found"}

    result = pricing_engine.dynamic_price(
        {"features": {f: 7 for f in product.get("features", [])}},
        persona={},
        product_name=product["name"]
    )

    evc = result["evc"]

    return {
        "product_cost": 12,
        "marketing_cost": 5,
        "distribution_cost": 3,
        "overhead_cost": 2,
        "target_margin": 40,
        "markup": 50,
        "market_avg_price": float(sum(result["competitors"])/len(result["competitors"])),
        "market_ceiling": max(result["competitors"]),
        "cost_based_price": evc["fair_price"],
        "value_adjusted_price": evc["premium_price"]
    }
