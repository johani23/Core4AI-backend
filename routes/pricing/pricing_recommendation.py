from fastapi import APIRouter, Request

router = APIRouter(prefix="/api/pricing/recommendation", tags=["Pricing Recommendation"])

@router.get("/{product_id}")
def recommendation_api(product_id: str, request: Request):

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

    price = result["final_price"]

    return {
        "suggested_price": price,
        "optimal_range": f"{round(price*0.9, 2)} – {round(price*1.1, 2)}",
        "confidence_score": 90,
        "strategy": "Hybrid ML Fusion Model",
        "strategy_comment": f"Elasticity={result['elasticity']}, EVC={result['evc']['recommended_price']}",
        "explanation": "Price derived from ML fusion of elasticity, competitor signals, and EVC.",
        "overpricing_warning": f"Above {round(price*1.15, 2)} SAR → demand likely to drop.",
        "underpricing_warning": f"Below {round(price*0.85, 2)} SAR → margin loss.",
        "final_recommendation": f"{price} SAR is the optimal ML-driven price."
    }
