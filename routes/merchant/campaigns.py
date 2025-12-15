# ============================================================================
# 💚 Core4.AI – Merchant Campaigns API
# FINAL STABLE VERSION (PRODUCT + DEMAND SUPPORTED)
# ============================================================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.campaign import Campaign
from models.product import Product
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

router = APIRouter(
    prefix="/api/merchant/campaigns",
    tags=["merchant-campaigns"]
)

# ============================================================================
# Pydantic Schema (DUAL MODE)
# ============================================================================
class CampaignCreate(BaseModel):
    # One of these must be provided
    product_id: Optional[int] = None
    intention_id: Optional[int] = None

    # Shared
    audience: str
    influencer: str
    ai_success_score: float

    # Product-based campaign
    recommended_price: Optional[float] = None

    # Demand-based campaign
    feature_text: Optional[str] = None
    target_price: Optional[float] = None


# ============================================================================
# GET all campaigns
# ============================================================================
@router.get("/")
def get_campaigns(db: Session = Depends(get_db)):
    campaigns = db.query(Campaign).order_by(Campaign.created_at.desc()).all()

    return [
        {
            "id": c.id,
            "product_id": c.product_id,
            "intention_id": c.intention_id,
            "audience": c.audience,
            "influencer": c.influencer,
            "recommended_price": c.recommended_price,
            "ai_success_score": c.ai_success_score,
            "status": c.status,
            "created_at": c.created_at,
        }
        for c in campaigns
    ]


# ============================================================================
# GET single campaign (CampaignSummary)
# ============================================================================
@router.get("/{campaign_id}")
def get_campaign(campaign_id: int, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    product = None
    mit_pricing = None

    if campaign.product_id:
        product = db.query(Product).filter(Product.id == campaign.product_id).first()
        if product:
            competitor_price = product.competitor_price or product.price

            mit_pricing = {
                "base_price": product.price,
                "competitor_price": competitor_price,
                "recommended_price": campaign.recommended_price,
                "market_floor": round(competitor_price * 0.92, 2),
                "market_ceiling": round(competitor_price * 1.18, 2),
                "conversion_lift": f"+{max(5, int(campaign.ai_success_score // 2))}%",
            }

    return {
        "id": campaign.id,
        "audience": campaign.audience,
        "influencer": campaign.influencer,
        "recommended_price": campaign.recommended_price,
        "ai_success_score": campaign.ai_success_score,
        "status": campaign.status,
        "created_at": campaign.created_at,

        # Used by CampaignSummary.jsx
        "product": product and {
            "id": product.id,
            "name": product.name,
            "category": product.category,
            "price": product.price,
            "competitor_price": product.competitor_price,
        },

        "mit_pricing": mit_pricing,

        "strategy": {
            "sequence": [campaign.audience],
        }
    }


# ============================================================================
# CREATE campaign (PRODUCT OR DEMAND)
# ============================================================================
@router.post("/")
def create_campaign(payload: CampaignCreate, db: Session = Depends(get_db)):
    # ------------------------------------------------------------
    # Validate mode
    # ------------------------------------------------------------
    if not payload.product_id and not payload.intention_id:
        raise HTTPException(
            status_code=400,
            detail="يجب اختيار منتج أو طلب سوق لإنشاء حملة"
        )

    if payload.product_id and not payload.recommended_price:
        raise HTTPException(
            status_code=400,
            detail="السعر المقترح مطلوب عند إنشاء حملة على منتج"
        )

    # ------------------------------------------------------------
    # Validate product if provided
    # ------------------------------------------------------------
    if payload.product_id:
        product = db.query(Product).filter(Product.id == payload.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="المنتج غير موجود")

    # ------------------------------------------------------------
    # Create campaign
    # ------------------------------------------------------------
    campaign = Campaign(
        product_id=payload.product_id,
        intention_id=payload.intention_id,
        audience=payload.audience,
        influencer=payload.influencer,
        recommended_price=payload.recommended_price or payload.target_price,
        ai_success_score=payload.ai_success_score,
        status="نشطة",
        created_at=datetime.utcnow(),
    )

    db.add(campaign)
    db.commit()
    db.refresh(campaign)

    return {
        "status": "created",
        "id": campaign.id,
    }
