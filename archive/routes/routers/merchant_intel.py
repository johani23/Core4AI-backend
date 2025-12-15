# ============================================================================
# 💚 Core4.AI – MerchantIntel API (v12 “Feature Pricing + Global Scanner”)
# ----------------------------------------------------------------------------
# • Closest Competitor Auto-Match
# • Feature-Based Price Delta
# • Market Weak Spots
# • Tribe Conversion Forecast
# • Saudi + GCC + Worldwide datasets
# • Value Score (1–100)
# ---------------------------------------------------------------------------

from fastapi import APIRouter, HTTPException
import random

router = APIRouter()

# ----------------------------------------------------------------------------
# Mock Global Database
# ----------------------------------------------------------------------------

GLOBAL_COMPETITORS = {
    "electronics": [
        {"name": "Anker Cam Pro", "price": 219, "region": "Worldwide"},
        {"name": "Xiaomi Smart Cam 2", "price": 199, "region": "China / GCC"},
        {"name": "Blink Mini", "price": 189, "region": "USA"},
        {"name": "Ezviz C3N", "price": 159, "region": "Middle East"},
    ],
    "fashion": [
        {"name": "Zara Tote", "price": 349, "region": "Worldwide"},
        {"name": "Mango Handbag", "price": 299, "region": "Europe"},
        {"name": "Charles & Keith Bag", "price": 399, "region": "Asia"},
    ],
    "outdoor": [
        {"name": "CampMaster Tent", "price": 550, "region": "GCC"},
        {"name": "AdventurePro Tent", "price": 499, "region": "Worldwide"},
    ],
    "events": [
        {"name": "MDL Beast Pass", "price": 180, "region": "Saudi"},
        {"name": "Summer Jam Ticket", "price": 250, "region": "USA"},
    ]
}

# ----------------------------------------------------------------------------
# Weak Spots
# ----------------------------------------------------------------------------
WEAK_SPOTS = [
    "Poor packaging quality",
    "Weak material durability",
    "No Arabic manual included",
    "Slow customer support response",
    "Limited regional warranty",
    "Overpriced compared to specs",
]

# ----------------------------------------------------------------------------
# Tribe Forecast
# ----------------------------------------------------------------------------
TRIBE_FORECAST = {
    "Fashionists": (65, 95),
    "Techy": (55, 90),
    "EventGoers": (50, 85),
    "Adventurers": (45, 80),
}

# ----------------------------------------------------------------------------
# Category Detection Helper
# ----------------------------------------------------------------------------
def detect_category(name: str):
    name = name.lower()
    if any(k in name for k in ["camera", "smart", "tech", "ai"]):
        return "electronics"
    elif any(k in name for k in ["bag", "tote", "dress", "shoe"]):
        return "fashion"
    elif any(k in name for k in ["tent", "camp", "outdoor"]):
        return "outdoor"
    elif any(k in name for k in ["ticket", "event", "pass"]):
        return "events"
    return "electronics"

# ----------------------------------------------------------------------------
# Main Endpoint
# ----------------------------------------------------------------------------
@router.get("/api/merchant/intel/{product_name}")
async def merchant_intel(product_name: str):

    category = detect_category(product_name)
    competitors = GLOBAL_COMPETITORS.get(category, [])

    if not competitors:
        raise HTTPException(404, "No competitors found")

    # Closest competitor
    closest = random.choice(competitors)

    # Feature delta pricing
    feature_strength = random.uniform(0.5, 1.6)
    feature_price_delta = round(feature_strength * 0.08 * closest["price"], 2)

    # Value score
    value_score = round(60 + feature_strength * 20 + random.uniform(-5, 5), 2)

    # Tribe forecast
    tribe_conversion = {
        tribe: random.randint(r[0], r[1]) for tribe, r in TRIBE_FORECAST.items()
    }

    return {
        "product": product_name,
        "category": category,
        "closest_competitor": closest,
        "feature_price_delta": feature_price_delta,
        "recommended_price": closest["price"] + feature_price_delta,
        "value_score": value_score,
        "market_weak_spots": random.sample(WEAK_SPOTS, 3),
        "tribe_forecast": tribe_conversion,
        "regions": ["Saudi Arabia", "GCC", "Worldwide"]
    }
