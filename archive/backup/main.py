# ======================================================================
# 💚 Core4.AI – main.py (v34 — ML Engine Integrated + No Circular Imports)
# ======================================================================

from fastapi import FastAPI, WebSocket, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import asyncio, logging, random, numpy as np

# ======================================================================
# ⚙️ ENGINE IMPORTS
# ======================================================================

from engines.competitor_db import CompetitorDB
from engines.feature_engine import FeatureEngine
from engines.persona_engine import PersonaEngine
from engines.tone_engine import ToneEngine

from engines.audience_fit_engine import AudienceFitEngine
from engines.quality_engine import QualityEngine
from engines.success_engine import SuccessEngine
from engines.funnel_engine import FunnelEngine
from engines.roi_engine import ROIEngine
from engines.cpa_engine import CPAEngine
from engines.breakeven_engine import BreakEvenEngine
from engines.scaling_engine import ScalingEngine
from engines.heatmap_engine import HeatmapEngine
from engines.budget_engine import BudgetEngine

from engines.narrative_engine import NarrativeEngine
from engines.autodraft_engine import AutoDraftEngine
from engines.copilot_engine import CoPilotEngine
from engines.autopilot_engine import AutoPilotEngine
from engines.megasummary_engine import MegaSummaryEngine
from engines.readiness_engine import ReadinessEngine
from engines.channelmix_engine import ChannelMixEngine

# ⭐ NEW ML ENGINE
from engines.pricing_engine_v22 import PricingEngineV22

# ======================================================================
# ⚙️ FASTAPI SETUP
# ======================================================================

app = FastAPI(title="Core4.AI – Merchant Intelligence API (v34 ML ENABLED)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logging.basicConfig(level=logging.INFO)

# ======================================================================
# ⚙️ ENGINE INITIALIZATION
# ======================================================================

competitor_db = CompetitorDB()
feature_engine = FeatureEngine()
persona_engine = PersonaEngine()
tone_engine = ToneEngine()

audience_fit_engine = AudienceFitEngine(persona_engine, feature_engine)
quality_engine = QualityEngine()
success_engine = SuccessEngine(quality_engine, audience_fit_engine)
funnel_engine = FunnelEngine()
roi_engine = ROIEngine()
cpa_engine = CPAEngine()
breakeven_engine = BreakEvenEngine()
scaling_engine = ScalingEngine()
heatmap_engine = HeatmapEngine()
budget_engine = BudgetEngine()

narrative_engine = NarrativeEngine(
    persona_engine, tone_engine, audience_fit_engine, feature_engine
)

autodraft_engine = AutoDraftEngine(narrative_engine)
copilot_engine = CoPilotEngine(tone_engine)
autopilot_engine = AutoPilotEngine(success_engine, scaling_engine)
megasummary_engine = MegaSummaryEngine()
readiness_engine = ReadinessEngine(success_engine, quality_engine)
channelmix_engine = ChannelMixEngine()

# ⭐ FIX: store ML engine inside app.state
app.state.pricing_engine = PricingEngineV22(
    competitor_db, feature_engine, audience_fit_engine, scaling_engine, roi_engine
)

# ======================================================================
# 🛒 PRODUCT SYSTEM (ALSO STORED IN STATE)
# ======================================================================

PRODUCTS = {}
app.state.products = PRODUCTS


class Product(BaseModel):
    product_id: str
    name: str
    price: float
    image_url: str
    features: List[str] = []
    description: str = ""
    category: str = ""


@app.post("/api/merchant/{merchant_id}/add-product")
def add_product(merchant_id: str, p: Product):
    PRODUCTS.setdefault(merchant_id, []).append(p.dict())
    return {"status": "ok"}


@app.get("/api/merchant/{merchant_id}/products")
def list_products(merchant_id: str):
    return PRODUCTS.get(merchant_id, [])

# ======================================================================
# 📊 Analytics Product List
# ======================================================================

@app.get("/api/analytics/products/{merchant_id}")
def analytics_products(merchant_id: str):
    prods = PRODUCTS.get(merchant_id, [])
    return [
        {
            "product_id": p["product_id"],
            "name": p["name"],
            "price": p["price"],
            "features": p.get("features", []),
            "description": p.get("description", ""),
            "image_url": p.get("image_url", ""),
        }
        for p in prods
    ]

# ======================================================================
# 💵 Update Product Price
# ======================================================================

class PriceUpdate(BaseModel):
    price: float

@app.post("/api/product/{product_id}/update-price")
def update_product_price(product_id: str, data: PriceUpdate):
    for merchant, plist in PRODUCTS.items():
        for p in plist:
            if p["product_id"] == product_id:
                p["price"] = data.price
                return {"status": "ok"}
    return {"status": "error", "message": "Product not found"}

# ======================================================================
# 🌐 ROUTER IMPORTS (AFTER ENGINES ARE READY)
# ======================================================================

from routes.pricing.pricing_overview import router as overview_router
from routes.pricing.pricing_breakdown import router as breakdown_router
from routes.pricing.pricing_elasticity import router as elasticity_router
from routes.pricing.pricing_demand_curve import router as demand_curve_router
from routes.pricing.pricing_evc import router as evc_router
from routes.pricing.pricing_recommendation import router as recommendation_router
from routes.pricing.pricing_commession import router as commission_router

# ======================================================================
# 🌐 ROUTER REGISTRATION
# ======================================================================

app.include_router(overview_router)
app.include_router(breakdown_router)
app.include_router(elasticity_router)
app.include_router(demand_curve_router)
app.include_router(evc_router)
app.include_router(recommendation_router)
app.include_router(commission_router)

# Add your existing buyer/creator routers below (unchanged)
# (kept clean and natural)
