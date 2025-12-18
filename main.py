# ============================================================================
# 💚 Core4.AI – Unified Backend API
# CLEAN PRODUCTION main.py (FINAL + MARKET INTENTIONS)
# Render-safe + Seeded
# ============================================================================

from contextlib import asynccontextmanager

# ============================
# DATABASE INITIALIZATION
# ============================
from db import Base, engine, SessionLocal

# IMPORTANT — Load ALL models BEFORE create_all()
from models import product
from models import campaign
from models.value_insights import ValueInsight
from models.product_pricing_mit import ProductPricingMIT
from models.market_intention import MarketIntention

# ============================
# SEED (DEMO PRODUCT)
# ============================
def seed_initial_data():
    db = SessionLocal()
    try:
        product_obj = db.query(product.Product).filter(product.Product.id == 1).first()
        if not product_obj:
            product_obj = product.Product(
                id=1,
                name="demo",
                price=4567,
                competitor_price=5678,
                category="test"
            )
            db.add(product_obj)

        mit = db.query(ProductPricingMIT).filter(ProductPricingMIT.product_id == 1).first()
        if not mit:
            mit = ProductPricingMIT(
                product_id=1,
                smart_price=4800,
                market_floor=4200,
                market_ceiling=5500
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
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Seed demo data
    seed_initial_data()

    yield  # App runs here

# ============================
# FASTAPI IMPORTS
# ============================
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ============================
# ROUTER IMPORTS
# ============================

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
    version="3.4",
    description="Unified backend with Demand-First Market Intention Engine",
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
        "version": "3.4",
        "database": "sqlite (/tmp)",
        "public_products": "/api/products",
        "market_intentions": "/api/market-intentions",
        "merchant_products": "/api/merchant/products",
        "audience_api": "/api/audience",
        "influence_api": "/api/influence",
        "rnd_api": "/api/rnd",
    }

# ============================
# SERVICE HEALTH CHECK
# ============================
@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "core4-backend",
        "version": "3.4"
    }
