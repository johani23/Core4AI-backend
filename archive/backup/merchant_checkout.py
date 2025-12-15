# ============================================================
# 💎 Core4.AI – Merchant Checkout API (v1.0)
# ------------------------------------------------------------
# • Product creation
# • Checkout session creation
# • Order confirmation
# • Creator/Tribe attribution
# • ROI-ready order data
# ============================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
import uuid

router = APIRouter()

# In-memory DB (replace with SQLAlchemy)
PRODUCTS = {}
ORDERS = {}

# -----------------------------
# Models
# -----------------------------
class ProductCreate(BaseModel):
    merchant_id: str
    name: str
    price: float
    image: str
    description: str

class CheckoutStart(BaseModel):
    product_id: str
    buyer_id: str | None = None
    creator_id: str | None = None
    tribe_id: str | None = None

class OrderConfirm(BaseModel):
    session_id: str
    status: str  # “paid” | “failed”


# -----------------------------
# Create Product
# -----------------------------
@router.post("/merchant/products/create")
def create_product(data: ProductCreate):
    product_id = str(uuid.uuid4())
    PRODUCTS[product_id] = {
        "id": product_id,
        "merchant_id": data.merchant_id,
        "name": data.name,
        "price": data.price,
        "image": data.image,
        "description": data.description,
        "created_at": datetime.utcnow()
    }
    return {"success": True, "product": PRODUCTS[product_id]}


# -----------------------------
# List Products for Merchant
# -----------------------------
@router.get("/merchant/{merchant_id}/products")
def list_products(merchant_id: str):
    return [p for p in PRODUCTS.values() if p["merchant_id"] == merchant_id]


# -----------------------------
# Start Checkout
# -----------------------------
@router.post("/checkout/start")
def start_checkout(data: CheckoutStart):

    if data.product_id not in PRODUCTS:
        raise HTTPException(404, "Product not found")

    session_id = str(uuid.uuid4())

    ORDERS[session_id] = {
        "session_id": session_id,
        "product": PRODUCTS[data.product_id],
        "merchant_id": PRODUCTS[data.product_id]["merchant_id"],
        "buyer_id": data.buyer_id,
        "creator_id": data.creator_id,
        "tribe_id": data.tribe_id,
        "status": "pending",
        "created_at": datetime.utcnow(),
    }

    return {
        "session_id": session_id,
        "checkout_url": f"https://payment-gateway.com/pay/{session_id}",
        "success": True,
    }


# -----------------------------
# Confirm Checkout
# -----------------------------
@router.post("/checkout/confirm")
def confirm_order(data: OrderConfirm):
    if data.session_id not in ORDERS:
        raise HTTPException(404, "Session not found")

    ORDERS[data.session_id]["status"] = data.status
    ORDERS[data.session_id]["confirmed_at"] = datetime.utcnow()

    return {"success": True, "order": ORDERS[data.session_id]}


# -----------------------------
# Merchant Order History
# -----------------------------
@router.get("/merchant/{merchant_id}/orders")
def merchant_orders(merchant_id: str):
    return [
        o for o in ORDERS.values()
        if o["merchant_id"] == merchant_id and o["status"] == "paid"
    ]


# -----------------------------
# Creator Sales (Attribution)
# -----------------------------
@router.get("/creator/{creator_id}/sales")
def creator_sales(creator_id: str):
    return [
        o for o in ORDERS.values()
        if o["creator_id"] == creator_id and o["status"] == "paid"
    ]
