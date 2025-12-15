# ============================================================================
# 💚 Core4AI – Orders API (Buyer Checkout + Merchant Orders View)
# ============================================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Create router
router = APIRouter(
    prefix="/api/orders",
    tags=["orders"]
)

# ============================
# Order Input Model
# ============================

class OrderInput(BaseModel):
    product_id: int
    qty: int = 1
    buyer_id: Optional[str] = None


# ============================
# In-Memory Storage (MVP)
# ============================

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
        "buyer_id": order.buyer_id or "guest",
        "timestamp": datetime.now().isoformat()
    }

    ORDERS.append(new_order)
    return {"status": "success", "order": new_order}


# ============================
# LIST ALL ORDERS (Merchant View)
# ============================

@router.get("/")
async def list_orders():
    return {"orders": ORDERS}


# ============================
# GET ORDER BY ID
# ============================

@router.get("/{order_id}")
async def get_order(order_id: int):
    for order in ORDERS:
        if order["id"] == order_id:
            return order

    raise HTTPException(status_code=404, detail="Order not found")
