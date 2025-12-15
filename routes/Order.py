# ============================================================================
# 💚 Core4AI – Orders API (Buyer Checkout & Merchant Orders View)
# ============================================================================

from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(
    prefix="/api/orders",
    tags=["orders"]
)

# ============================
# MODELS
# ============================

class OrderInput(BaseModel):
    product_id: int
    qty: int = 1
    buyer_id: str | None = None

# Temporary in-memory store (MVP)
ORDERS = []

# ============================
# CREATE ORDER
# ============================

@router.post("/")
async def create_order(order: OrderInput):
    new_order = {
        "id": len(ORDERS) + 1,
        "product_id": order.product_id,
        "qty": order.qty,
        "buyer_id": order.buyer_id,
        "timestamp": datetime.now().isoformat()
    }
    ORDERS.append(new_order)
    return {"status": "success", "order": new_order}

# ============================
# LIST ORDERS (Merchant Dashboard)
# ============================

@router.get("/")
async def list_orders():
    return ORDERS

# ============================
# GET ORDER BY ID
# ============================

@router.get("/{order_id}")
async def get_order(order_id: int):
    for o in ORDERS:
        if o["id"] == order_id:
            return o
    return {"error": "Order not found"}
s