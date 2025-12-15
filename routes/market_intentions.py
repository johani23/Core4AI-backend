# ============================================================================
# 🔵 Core4.AI – Market Intentions API
# Buyer creates demand • Merchant reads opportunities
# ============================================================================

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from db import get_db
from models.market_intention import MarketIntention

router = APIRouter(
    prefix="/market-intentions",
    tags=["market-intentions"]
)

# ----------------------------------------------------------------------------
# CREATE INTENTION (BuyerRND)
# ----------------------------------------------------------------------------
@router.post("/")
def create_intention(payload: dict, db: Session = Depends(get_db)):
    intention = MarketIntention(
        feature_text=payload.get("feature_text"),
        normalized_features=payload.get("normalized_features"),
        target_price=payload.get("target_price"),
        max_price=payload.get("max_price"),
        quantity_interest=payload.get("quantity_interest", 1),
        time_horizon=payload.get("time_horizon"),
        buyer_cluster=payload.get("buyer_cluster"),
    )

    db.add(intention)
    db.commit()
    db.refresh(intention)

    return {"status": "created", "id": intention.id}


# ----------------------------------------------------------------------------
# LIST OPEN INTENTIONS (Merchant)
# ----------------------------------------------------------------------------
@router.get("/")
def list_intentions(db: Session = Depends(get_db)):
    intentions = (
        db.query(MarketIntention)
        .filter(MarketIntention.status == "open")
        .order_by(MarketIntention.created_at.desc())
        .all()
    )

    return [
        {
            "id": i.id,
            "feature_text": i.feature_text,
            "normalized_features": i.normalized_features,
            "target_price": i.target_price,
            "max_price": i.max_price,
            "quantity_interest": i.quantity_interest,
            "time_horizon": i.time_horizon,
            "buyer_cluster": i.buyer_cluster,
            "created_at": i.created_at,
        }
        for i in intentions
    ]
