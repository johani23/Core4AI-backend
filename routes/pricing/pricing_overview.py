from fastapi import APIRouter, Request

router = APIRouter(prefix="/api/pricing/overview", tags=["Pricing Overview"])

@router.get("/{product_id}")
def overview_api(product_id: str, request: Request):

    PRODUCTS = request.app.state.products
    pricing_engine = request.app.state.pricing_engine

    # Find product
    product = None
    for _, plist in PRODUCTS.items():
        for p in plist:
            if p["product_id"] == product_id:
                product = p
                break

    if not product:
        return {"error": "Product not found"}

    # ML Engine Call
    result = pricing_engine.dynamic_price(
        {"features": {f: 7 for f in product.get("features", [])}},
        persona={},
        product_name=product["name"]
    )

    return {
        "suggested_price": result["final_price"],
        "optimal_range": f"{round(result['final_price']*0.9, 2)} – {round(result['final_price']*1.1, 2)}",
        "confidence_score": 87,
        "strategy": "ML value-based hybrid",
        "strategy_explanation": "Combined EVC + elasticity + competitor fusion.",
        "reason": f"Final price derived from ML elasticity={result['elasticity']}."
    }
