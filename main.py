# ============================================================================
# 💚 Core4.AI – Unified Backend API
# CLEAN PRODUCTION main.py (FINAL – PILOT + BETA HARDENING READY)
# Render-safe + Seeded
# ============================================================================
# main.py ONLY wires APIs (no judgment here)
# ============================================================================

from contextlib import asynccontextmanager
import os
import importlib

# ============================
# DATABASE INITIALIZATION
# ============================
from db import Base, engine, SessionLocal


# ============================
# SAFE IMPORT RESOLVER (FIX ONCE FOREVER)
# ============================
def _imp(*candidates):
    """
    Try import module paths in order; return first that works.
    Raises the last error if none work.
    """
    last_err = None
    for c in candidates:
        try:
            return importlib.import_module(c)
        except ModuleNotFoundError as e:
            last_err = e
    raise last_err


# ----------------------------
# Models (try flat layout first, then app layout)
# ----------------------------
product = _imp("models.product", "app.models.product")
campaign = _imp("models.campaign", "app.models.campaign")

# Signal model name sometimes differs (signal.py vs signals.py)
signal_mod = _imp("models.signal", "models.signals", "app.models.signal", "app.models.signals")

ValueInsight = _imp("models.value_insights", "app.models.value_insights").ValueInsight
ProductPricingMIT = _imp("models.product_pricing_mit", "app.models.product_pricing_mit").ProductPricingMIT
MarketIntention = _imp("models.market_intention", "app.models.market_intention").MarketIntention
GovernanceDecision = _imp("models.governance_decision", "app.models.governance_decision").GovernanceDecision
GovernanceReview = _imp("models.governance_review", "app.models.governance_review").GovernanceReview
TribeSignal = _imp("models.tribe_signal", "app.models.tribe_signal").TribeSignal

Signal = getattr(signal_mod, "Signal")


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
                category="test",
                image_url="https://images.unsplash.com/photo-1523275335684-37898b6baf30",
            )
            db.add(product_obj)

        mit = db.query(ProductPricingMIT).filter(ProductPricingMIT.product_id == 1).first()

        if not mit:
            mit = ProductPricingMIT(
                product_id=1,
                base_price=4567,
                competitor_price=5678,
                smart_price=4800,
                market_floor=4200,
                market_ceiling=5500,
                tribe_hotness=0.6,
                conversion_lift=0.12,
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

    Base.metadata.create_all(bind=engine)
    seed_initial_data()
    yield


# ============================
# FASTAPI IMPORTS
# ============================
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# ============================
# ROUTER IMPORTS (ALSO RESOLVED SAFELY)
# ============================
signals_router = _imp("routes.signals", "app.routes.signals").router

# Governance (some repos keep these under app.routes)
governance_queue_router = _imp("app.routes.governance_queue", "routes.governance_queue").router
governance_debug_router = _imp("app.routes.governance_debug", "routes.governance_debug").router
governance_metrics_router = _imp("app.routes.governance_metrics", "routes.governance_metrics").router

products_router = _imp("routes.products", "app.routes.products").router
orders_router = _imp("routes.orders", "app.routes.orders").router
pulse_router = _imp("routes.pulse", "app.routes.pulse").router

market_intentions_router = _imp("routes.market_intentions", "app.routes.market_intentions").router
creator_api_router = _imp("routes.creator_api", "app.routes.creator_api").router

merchant_products_router = _imp("routes.merchant.products", "app.routes.merchant.products").router
merchant_campaigns_router = _imp("routes.merchant.campaigns", "app.routes.merchant.campaigns").router
merchant_analytics_router = _imp("routes.merchant.analytics", "app.routes.merchant.analytics").router
merchant_analytics_v2_router = _imp("routes.merchant.analytics_v2", "app.routes.merchant.analytics_v2").router
merchant_commission_router = _imp("routes.merchant.commission", "app.routes.merchant.commission").router

audience_router = _imp("routes.audience", "app.routes.audience").router
influence_router = _imp("routes.influence", "app.routes.influence").router

creator_legacy_router = _imp("routes.creator", "app.routes.creator").router
analytics_legacy_router = _imp("routes.analytics", "app.routes.analytics").router

rnd_router = _imp("routes.rnd_routes", "app.routes.rnd_routes").router


# ============================
# FASTAPI INITIALIZATION
# ============================
app = FastAPI(
    title="Core4.AI Backend API",
    version="3.5-beta-hardened",
    description=(
        "Unified backend API with Signal Ingestion, "
        "Human-in-the-loop Governance, Tribe-Governed Pricing, "
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
app.include_router(signals_router, prefix="/api")

app.include_router(governance_queue_router, prefix="/api")
app.include_router(governance_debug_router, prefix="/api")
app.include_router(governance_metrics_router, prefix="/api")

app.include_router(products_router, prefix="/api")
app.include_router(orders_router, prefix="/api")
app.include_router(pulse_router, prefix="/api")

app.include_router(market_intentions_router, prefix="/api")
app.include_router(creator_api_router, prefix="/api/creator")

app.include_router(merchant_products_router)
app.include_router(merchant_campaigns_router)
app.include_router(merchant_analytics_router)
app.include_router(merchant_analytics_v2_router)
app.include_router(merchant_commission_router)

app.include_router(audience_router, prefix="/api/audience")
app.include_router(influence_router, prefix="/api/influence")

app.include_router(creator_legacy_router, prefix="/api")
app.include_router(analytics_legacy_router, prefix="/api")

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
        "pricing_engine": "tribe-governed (internal)",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "core4-backend",
        "version": "3.5-beta-hardened",
    }


@app.get("/api/health")
def api_health():
    return health()
