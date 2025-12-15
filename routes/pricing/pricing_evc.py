from fastapi import APIRouter, Request

router = APIRouter(prefix="/api/pricing/evc", tags=["Pricing EVC"])

@router.get("/{product_id}")
def evc_api(product_id: str, request: Request):

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
        "reference_price": evc["reference_price"],
        "diff_value": evc["differentiation_value"],
        "features": evc["utilities"],
        "total_evc": evc["total_evc"],
        "fair_price": evc["fair_price"],
        "premium_price": evc["premium_price"],
        "recommendation": f"{evc['recommended_price']} SAR is the EVC-based optimal price."
    }
