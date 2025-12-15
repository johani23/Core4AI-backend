from fastapi import APIRouter, Request

router = APIRouter(prefix="/api/pricing/demand-curve", tags=["Pricing Demand Curve"])

@router.get("/{product_id}")
def demand_curve_api(product_id: str, request: Request):

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

    curve = result["curve"]

    return {
        "summary": "Demand curve generated using ML polynomial regression.",
        "points": curve["curve"]["points"],
        "zone_low": curve["zones"]["zone_low"],
        "zone_optimal": curve["zones"]["zone_optimal"],
        "zone_high": curve["zones"]["zone_high"],
        "sensitivity_label": result["sensitivity"],
        "sensitivity_comment": "Derived from curve slope."
    }
