from fastapi import APIRouter
from audience_engine import generate_dynamic_persona, compute_heatmap_score

router = APIRouter()

FAKE_EVENTS_DB = {}  # buyer_id -> events

@router.post("/event")
def track_event(event: dict):
    buyer_id = event["payload"]["buyer_id"]
    FAKE_EVENTS_DB.setdefault(buyer_id, [])
    FAKE_EVENTS_DB[buyer_id].append(event)
    return {"status": "ok"}

@router.get("/{buyer_id}/persona")
def get_dynamic_persona(buyer_id: str):
    events = FAKE_EVENTS_DB.get(buyer_id, [])
    persona = generate_dynamic_persona(buyer_id, events)
    return persona

@router.get("/{buyer_id}/heatmap")
def get_heatmap(buyer_id: str):
    events = FAKE_EVENTS_DB.get(buyer_id, [])
    score = compute_heatmap_score(events)
    return {"buyer_id": buyer_id, "heat_score": score}
