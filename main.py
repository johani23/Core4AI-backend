# ============================================================================
# 💚 Core4.AI – Unified Backend API
# CLEAN PRODUCTION main.py (FINAL – PILOT + BETA HARDENING READY)
# Render-safe + Seeded
# ============================================================================
# NOTE:
# - Signal extraction lives in app/engines/signals/
# - Governance logic lives in app/engines/governance/
# - Pricing governance (Tribes) lives in app/engines/pricing/
# - main.py ONLY wires APIs (no judgment here)
# ============================================================================

from contextlib import asynccontextmanager
import os

# ============================
# DATABASE INITIALIZATION
# ============================
from db import Base, engine, SessionLocal

# IMPORTANT — Load ALL models BEFORE create_all()
from app.models import product
from app.models import campaign
from app.models.signal import Signal
from app.models.value_insights import ValueInsight
from app.models.product_pricing_mit import ProductPricingMIT
from app.models.market_intention import MarketIntention
from app.models.governance_decision import GovernanceDecision
from app.models.governance_review import GovernanceReview
from app.models.tribe_signal import TribeSignal

# 🔐 Tribe Governance Signal (Pricing + Trust)



# ============================
# SEED (DEMO PRODUCT)
# ============================
def seed_initial_data():
    db = SessionLocal()
    try:
        product_obj = (
            db.query(product.Product)
            .filter(product.Product.id == 1)
            .first()
        )

        if not product_obj:
            product_obj = product.Product(
                id=1,
                name="demo",
                price=4567,
                competitor_price=5678,
                category="test",
                image_url="https://images.unsplash.com/photo-1523275335684-37898b6baf30"
            )
            db.add(product_obj)

        mit = (
            db.query(ProductPricingMIT)
            .filter(ProductPricingMIT.product_id == 1)
            .first()
        )

        if not mit:
            mit = ProductPricingMIT(
                product_id=1,
                base_price=4567,
                competitor_price=5678,
                smart_price=4800,
                market_floor=4200,
                market_ceiling=5500,
                tribe_hotness=0.6,
                conversion_lift=0.12
            )
            db.add(mit)

        db.commit()
    finally:
        db.close()


# ============================
# FASTAPI LIFESPAN
# ============================
@asynccontextmanager
async def lifespan(app):
    # 🔥 FORCE RESET SQLITE (DEV / DEMO ONLY)
    db_path = "/tmp/core4.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    # Create all tables (includes TribeSignal)
    Base.metadata.create_all(bind=engine)

    # Seed demo data
    seed_initial_data()

    yield


# ============================
# FASTAPI IMPORTS
# ============================
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# ============================
# ROUTER IMPORTS
# ============================

# Signals (Pilot – Governance / Regret / Activity)
from routes.signals import router as signals_router

# Governance (Beta Hardening)
from app.routes.governance_queue import router as governance_queue_router
from app.routes.governance_debug import router as governance_debug_router
from app.routes.governance_metrics import router as governance_metrics_router

# Public Buyer APIs
from routes.products import router as products_router
from routes.orders import router as orders_router
from routes.pulse import router as pulse_router

# Market Intentions
from routes.market_intentions import router as market_intentions_router

# Creator APIs
from routes.creator_api import router as creator_api_router

# Merchant APIs
from routes.merchant.products import router as merchant_products_router
from routes.merchant.campaigns import router as merchant_campaigns_router
from routes.merchant.analytics import router as merchant_analytics_router
from routes.merchant.analytics_v2 import router as merchant_analytics_v2_router
from routes.merchant.commission import router as merchant_commission_router

# Audience + Influence APIs
from routes.audience import router as audience_router
from routes.influence import router as influence_router

# Legacy APIs
from routes.creator import router as creator_legacy_router
from routes.analytics import router as analytics_legacy_router

# MIT / R&D APIs
from routes.rnd_routes import router as rnd_router


# ============================
# FASTAPI INITIALIZATION
# ============================
app = FastAPI(
    title="Core4.AI Backend API",
    version="3.5-beta-hardened",
    description=(
        "Unified backend API with Signal Ingestion, "
        "Human-in-the-loop Governance, "
        "Tribe-Governed Pricing, "
        "Explainability, and Operational Metrics"
    ),
    lifespan=lifespan,
)


# ============================
# CORS SETTINGS
# ============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================
# ROUTE REGISTRATION
# ============================

# 🔔 Signals (Pilot)
app.include_router(signals_router, prefix="/api")

# 🧠 Governance (Beta Hardening)
app.include_router(governance_queue_router, prefix="/api")
app.include_router(governance_debug_router, prefix="/api")
app.include_router(governance_metrics_router, prefix="/api")

# Public Buyer APIs
app.include_router(products_router, prefix="/api")
app.include_router(orders_router, prefix="/api")
app.include_router(pulse_router, prefix="/api")

# Market Intentions
app.include_router(market_intentions_router, prefix="/api")

# Creator APIs
app.include_router(creator_api_router, prefix="/api/creator")

# Merchant APIs
app.include_router(merchant_products_router)
app.include_router(merchant_campaigns_router)
app.include_router(merchant_analytics_router)
app.include_router(merchant_analytics_v2_router)
app.include_router(merchant_commission_router)

# Audience + Influence
app.include_router(audience_router, prefix="/api/audience")
app.include_router(influence_router, prefix="/api/influence")

# Legacy APIs
app.include_router(creator_legacy_router, prefix="/api")
app.include_router(analytics_legacy_router, prefix="/api")

# MIT / R&D APIs
app.include_router(rnd_router, prefix="/api/rnd")


# ============================
# ROOT HEALTH CHECK
# ============================
@app.get("/")
def root():
    return {
        "status": "Core4 Backend Running",
        "version": "3.5-beta-hardened",
        "database": "sqlite (/tmp)",
        "signals_api": "/api/signals",
        "governance_queue": "/api/governance/queue",
        "governance_debug": "/api/governance/debug",
        "governance_metrics": "/api/governance/metrics",
        "public_products": "/api/products",
        "market_intentions": "/api/market-intentions",
        "merchant_products": "/api/merchant/products",
        "audience_api": "/api/audience",
        "influence_api": "/api/influence",
        "rnd_api": "/api/rnd",
        "pricing_engine": "tribe-governed (internal)",
    }


# ============================
# SERVICE HEALTH CHECK
# ============================
@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "core4-backend",
        "version": "3.5-beta-hardened"
    }

@app.get("/api/health")
def api_health():
    return health()
