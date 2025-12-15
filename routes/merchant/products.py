# ============================================================================
# Core4.AI – Merchant Products API
# FINAL STABLE VERSION (NO REDIRECTS / NO DUPLICATES / NO NaN)
# ============================================================================

from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import text
import json

from db import get_db
from models.product import Product

router = APIRouter(
    prefix="/api/merchant/products",
    tags=["merchant-products"]
)

# ============================================================================
# GET ALL PRODUCTS
# ============================================================================
@router.get("/")
def get_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "price": float(p.price),
            "category": p.category,
            "competitor_price": float(p.competitor_price or p.price),
        }
        for p in products
    ]

# ============================================================================
# GET SINGLE PRODUCT
# ============================================================================
@router.get("/{product_id}")
def get_single_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {
        "id": product.id,
        "name": product.name,
        "price": float(product.price),
        "category": product.category,
        "description": product.description,
        "competitor_price": float(product.competitor_price or product.price),
        "features": json.loads(product.features) if product.features else [],
    }

# ============================================================================
# POST — CREATE PRODUCT  (✅ FIXED PATH)
# ============================================================================
@router.post("/")
def create_product(
    name: str = Form(...),
    price: float = Form(...),
    category: str = Form(""),
    description: str = Form(""),
    competitor_price: float = Form(None),
    features: str = Form("[]"),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    product = Product(
        name=name,
        price=float(price),
        category=category,
        description=description,
        competitor_price=float(competitor_price) if competitor_price else float(price),
        features=features,
        image_url=None,
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return {
        "status": "created",
        "id": product.id,
    }

# ============================================================================
# POST — CALCULATE & SAVE MIT
# ============================================================================
@router.post("/{product_id}/mit")
def calculate_and_save_mit(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    base_price = float(product.price)
    competitor_price = float(product.competitor_price or base_price)

    market_floor = round(competitor_price * 0.92, 2)
    market_ceiling = round(competitor_price * 1.18, 2)

    smart_price = round(
        competitor_price * 0.6 + base_price * 0.4,
        2
    )

    db.execute(
        text("""
            INSERT INTO product_pricing_mit
            (product_id, base_price, competitor_price,
             smart_price, market_floor, market_ceiling,
             tribe_hotness, conversion_lift)
            VALUES
            (:pid, :base, :comp, :smart, :floor, :ceiling, :tribe, :lift)
        """),
        {
            "pid": product_id,
            "base": base_price,
            "comp": competitor_price,
            "smart": smart_price,
            "floor": market_floor,
            "ceiling": market_ceiling,
            "tribe": "General",
            "lift": "+15%",
        }
    )

    db.commit()

    return {
        "status": "calculated",
        "smart_price": smart_price,
    }

# ============================================================================
# GET MIT — SAFE (NO NaN / NO 500)
# ============================================================================
@router.get("/{product_id}/mit")
def get_mit_price(product_id: int, db: Session = Depends(get_db)):
    row = db.execute(
        text("""
            SELECT smart_price, market_floor, market_ceiling, competitor_price
            FROM product_pricing_mit
            WHERE product_id = :pid
            ORDER BY created_at DESC
            LIMIT 1
        """),
        {"pid": product_id}
    ).fetchone()

    if not row:
        return {
            "status": "not_ready",
            "smart_price": None,
            "market_floor": None,
            "market_ceiling": None,
            "competitor_price": None,
        }

    return {
        "status": "ready",
        "smart_price": float(row.smart_price),
        "market_floor": float(row.market_floor),
        "market_ceiling": float(row.market_ceiling),
        "competitor_price": float(row.competitor_price),
    }
