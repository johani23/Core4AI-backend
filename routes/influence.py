# ============================================================================
# 💚 Core4.AI – Influence Router v1.0
# ============================================================================

from fastapi import APIRouter
from influence_engine import compute_influence, get_influence_tier
from audience_engine import generate_dynamic_persona
from routes.audience import FAKE_EVENTS_DB

router = APIRouter()

@router.get("/{buyer_id}/influence")
def get_influence_data(buyer_id: str):
    events = FAKE_EVENTS_DB.get(buyer_id, [])
    persona = generate_dynamic_persona(buyer_id, events)

    score = compute_influence(events, persona)
    tier = get_influence_tier(score)

    return {
        "buyer_id": buyer_id,
        "influence_score": score,
        "tier": tier,
        "persona": persona,
    }
