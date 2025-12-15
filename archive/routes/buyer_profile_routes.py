# ============================================================
# 💚 Core4.AI – Buyer Profile Module (v2.0 FINAL)
# ============================================================

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
import datetime

router = APIRouter(prefix="/api/buyer", tags=["Buyer"])

# ------------------------------------------------------------
# GLOBAL BUYER STORE
# ------------------------------------------------------------
BUYERS = {}

# ------------------------------------------------------------
# DATA MODEL
# ------------------------------------------------------------
class BuyerProfile(BaseModel):
    buyer_id: str
    name: Optional[str] = "Guest"
    tokens: float = 0.0
    tested_products: List[str] = []
    r_and_d_score: float = 0.0
    referral_success: int = 0
    influencer_ready: bool = False
    tribe_fit: Optional[str] = None
    events: List[dict] = []


# ------------------------------------------------------------
# EVENT LOGGER (GLOBAL)
# ------------------------------------------------------------
def log_event(buyer_id: str, type: str, description: str, icon="🟢"):
    if buyer_id not in BUYERS:
        return
    
    BUYERS[buyer_id]["events"].append({
        "type": type,
        "description": description,
        "icon": icon,
        "timestamp": datetime.datetime.now().isoformat()
    })


# ------------------------------------------------------------
# AUTO-CREATE DEFAULT BUYER
# ------------------------------------------------------------
DEFAULT_BUYER_ID = "buyer_001"

if DEFAULT_BUYER_ID not in BUYERS:
    BUYERS[DEFAULT_BUYER_ID] = {
        "buyer_id": DEFAULT_BUYER_ID,
        "name": "Ahmad",
        "tokens": 0,
        "tested_products": [],
        "r_and_d_score": 0,
        "referral_success": 0,
        "tribe_fit": None,
        "influencer_ready": False,
        "events": []
    }
    log_event(DEFAULT_BUYER_ID, "Profile Auto-Init", "Default buyer created.", "✨")


# ------------------------------------------------------------
# CREATE BUYER
# ------------------------------------------------------------
@router.post("/create")
def create_buyer(profile: BuyerProfile):
    BUYERS[profile.buyer_id] = profile.dict()
    log_event(profile.buyer_id, "Profile Created", "New buyer profile created.", "🆕")
    return {"status": "created", "profile": profile}


# ------------------------------------------------------------
# GET PROFILE
# ------------------------------------------------------------
@router.get("/{buyer_id}")
def get_profile(buyer_id: str):
    return BUYERS.get(buyer_id, {"error": "Buyer not found"})


# ------------------------------------------------------------
# ADD TESTED PRODUCT
# ------------------------------------------------------------
@router.post("/{buyer_id}/test/{product_id}")
def test_product(buyer_id: str, product_id: str):
    if buyer_id not in BUYERS:
        return {"error": "Buyer not found"}

    BUYERS[buyer_id]["tested_products"].append(product_id)
    log_event(buyer_id, "Product Tested", f"Tested product {product_id}", "🧪")
    return BUYERS[buyer_id]


# ------------------------------------------------------------
# ADD TOKENS
# ------------------------------------------------------------
@router.post("/{buyer_id}/tokens/{amount}")
def add_tokens(buyer_id: str, amount: float):
    if buyer_id not in BUYERS:
        return {"error": "Buyer not found"}

    BUYERS[buyer_id]["tokens"] += amount
    log_event(buyer_id, "Tokens Earned", f"+{amount} tokens", "💰")
    return BUYERS[buyer_id]
