from fastapi import APIRouter, Request

router = APIRouter(prefix="/api/pricing/elasticity", tags=["Pricing Elasticity"])

@router.get("/{product_id}")
def elasticity_api(product_id: str, request: Request):

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

    elasticity_val = result["elasticity"]

    return {
        "current_price": result["final_price"],
        "current_demand": 100,
        "elasticity": elasticity_val,
        "elasticity_label": result["sensitivity"],
        "elasticity_comment": "Elasticity derived from ML regression model.",
        "plus_10pct_demand": int(100 * (1 + elasticity_val * 0.10)),
        "minus_10pct_demand": int(100 * (1 - elasticity_val * 0.10)),
        "plus_10pct_revenue": round(result["final_price"]*1.1 * (100 * (1 + elasticity_val * 0.10)), 2),
        "minus_10pct_revenue": round(result["final_price"]*0.9 * (100 * (1 - elasticity_val * 0.10)), 2),
        "recommendation": "Leverage elasticity to guide price movement."
    }
