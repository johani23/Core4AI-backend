# ============================================================
# 💚 Core4.AI – merchant_marketing.py
# ------------------------------------------------------------
# • AI Marketing Plan Generator
# • Influencer Recommendation Engine
# • Product Classification Logic
# • Audience Cluster Suggestions
# ============================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import random

router = APIRouter(prefix="/api/merchant", tags=["Marketing"])

# ----------------------------------------------------------------
# 🧬 Sample creator db (temporary mock)
# ----------------------------------------------------------------
CREATORS = [
    {"name": "Sara Reviews", "tribe": "Fashionists", "score": 92},
    {"name": "TechGuru Saad", "tribe": "Techy", "score": 88},
    {"name": "Nour Style", "tribe": "Fashionists", "score": 80},
    {"name": "AdventurePro", "tribe": "Adventurers", "score": 94},
    {"name": "FamilyLife KSA", "tribe": "EventGoers", "score": 77},
]

TRIBE_CLUSTERS = {
    "new": ["Techy", "Fashionists", "Adventurers"],
    "launch": ["EventGoers", "Fashionists"],
    "brand_reinforce": ["Fashionists", "Techy"],
}


# ------------------------------------------------------------
# 📌 Models
# ------------------------------------------------------------
class MarketingPlanRequest(BaseModel):
    product_name: str
    objective: str
    message: str


# ============================================================
# 🧠 1) AI MARKETING PLAN
# ============================================================
@router.post("/marketing_plan")
async def generate_marketing_plan(payload: MarketingPlanRequest):
    """Create a full AI-powered marketing plan"""

    objective = payload.objective

    content_map = {
        "new": ["Unboxing", "TikTok Short Review", "Quick Demo"],
        "launch": ["Teaser Ads", "Countdown Posts", "Influencer Sampling"],
        "brand_reinforce": ["Lifestyle Reels", "Experience-Based Videos", "Testimonial Clips"],
    }

    posting_times = ["4-6 PM", "8-10 PM", "Weekend Noon"]

    plan = {
        "recommended_content_types": content_map.get(objective, []),
        "ideal_posting_times": posting_times,
        "target_tribes": TRIBE_CLUSTERS.get(objective, []),
        "estimated_budget": f"{random.randint(2500, 8000)} SAR",
        "ideal_creators_level": "Mid-tier + Nano creators",
    }

    return {"ai_marketing_plan": plan}


# ============================================================
# 🧲 2) Influencer Recommendations
# ============================================================
@router.get("/suggest_influencers/{product_name}")
async def suggest_influencers(product_name: str):

    # Smart simple matching – TEMP
    # In final: match by tribe affinity + D-index + product category
    result = sorted(
        CREATORS,
        key=lambda x: x["score"],
        reverse=True
    )[:4]

    return {"recommended_influencers": result}


# ============================================================
# 🎯 3) Audience Cluster Suggestions
# ============================================================
@router.get("/audience_clusters/{product_name}")
async def get_audience_clusters(product_name: str):

    clusters = [
        "Young Professionals",
        "Saudi Mothers 25-40",
        "Gen-Z Students",
        "Tech Enthusiasts",
        "Luxury Lifestyle Seekers",
    ]

    random.shuffle(clusters)
    result = clusters[:3]

    return {"audience_segments": result}
# ============================================================
# 📢 4) Merchant Campaigns – Mock Campaign Data
# ============================================================

CAMPAIGNS = [
    {
        "id": 1,
        "title": "Winter Launch Campaign",
        "objective": "launch",
        "budget": "5000 SAR",
        "status": "active",
        "tribes": ["Fashionists", "EventGoers"],
        "creators": ["Sara Reviews", "Nour Style"],
    },
    {
        "id": 2,
        "title": "Tech Product Awareness",
        "objective": "brand_reinforce",
        "budget": "3200 SAR",
        "status": "draft",
        "tribes": ["Techy"],
        "creators": ["TechGuru Saad"],
    }
]

@router.get("/campaigns")
async def get_campaigns():
    """Return all merchant campaigns"""
    return {"campaigns": CAMPAIGNS}
