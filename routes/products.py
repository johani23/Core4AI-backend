# ============================================================================
# 🟢 Core4.AI – Public Products API (BuyerFeed)
# READ-ONLY • Safe • Shared with Merchant DB
# ============================================================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import json

from db import get_db
from models.product import Product

router = APIRouter(
    prefix="/products",
    tags=["products"]
)


# ----------------------------------------------------------------------------
# GET ALL PRODUCTS (PUBLIC)
# ----------------------------------------------------------------------------
@router.get("/")
def list_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    output = []

    for p in products:
        output.append({
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "category": p.category,
            "description": p.description,
            "features": json.loads(p.features) if p.features else [],
            "image_url": p.image_url,
            "rating": 4.7,           # placeholder
            "stock": 5,              # placeholder
            "tribe": "General",      # placeholder
            "drop": "-10%"           # placeholder
        })

    return output


# ----------------------------------------------------------------------------
# GET SINGLE PRODUCT (PUBLIC)
# ----------------------------------------------------------------------------
@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")

    return {
        "id": p.id,
        "name": p.name,
        "price": p.price,
        "category": p.category,
        "description": p.description,
        "features": json.loads(p.features) if p.features else [],
        "image_url": p.image_url,
        "rating": 4.7,
        "stock": 5,
        "tribe": "General",
        "drop": "-10%"
    }
