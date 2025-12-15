# ============================================================
# 💎 Core4.AI – mentor_engine.py (MVP-85 “Mentorship Analytics Engine”)
# ------------------------------------------------------------
# ✅ Retains MVP-84 dynamic logic
# ✅ Adds analytics aggregation:
#      • cumulative growth per mentor
#      • mentor efficiency index
#      • retention score (active apprentices / total)
# ✅ New endpoints: /mentor/analytics  &  /mentor/history/<mentor>
# ============================================================

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from datetime import datetime, timedelta
import asyncio, random, json
from modules import creator

router = APIRouter()

# ------------------------------------------------------------
# 🧩 Shared state
# ------------------------------------------------------------
active_radars = set()
axes = ["Skill", "Creativity", "Consistency", "Empathy", "Influence"]
mentor_feed = []   # live log of mentorship events
mentor_stats = {}  # aggregated analytics {mentor: {...}}

# ------------------------------------------------------------
# 🔍 Dynamic pairing (same as before)
# ------------------------------------------------------------
def get_dynamic_pairs():
    all_creators = creator.get_all_creators()
    mentors = [c for c in all_creators if c["score"] >= 65]
    apprentices = [c for c in all_creators if c["score"] < 65]

    pairs = []
    for m in mentors:
        if not apprentices:
            break
        a = random.choice(apprentices)
        gap = round(m["score"] - a["score"], 1)
        pairs.append(
            {
                "mentor": m["name"],
                "apprentice": a["name"],
                "axis": random.choice(axes),
                "growth": max(3, min(20, int(gap / 2))),
            }
        )
    return pairs


def random_radar_payload():
    return [
        {
            "axis": axis,
            "mentor": random.randint(60, 100),
            "apprentice": random.randint(30, 90),
        }
        for axis in axes
    ]

# ------------------------------------------------------------
# 📊 Analytics Builders
# ------------------------------------------------------------
def update_mentor_stats(event):
    """Aggregate analytics for each mentor after a growth pulse."""
    m = event["mentor"]
    s = mentor_stats.setdefault(
        m, {"total_growth": 0, "sessions": 0, "apprentices": set(), "history": []}
    )

    s["total_growth"] += event["growth"]
    s["sessions"] += 1
    s["apprentices"].add(event["apprentice"])
    s["history"].append(event)

def compute_efficiency(m):
    """Return mentor efficiency index = avg growth / number of apprentices."""
    data = mentor_stats.get(m)
    if not data:
        return 0.0
    active = max(1, len(data["apprentices"]))
    avg_growth = data["total_growth"] / max(1, data["sessions"])
    return round(avg_growth / active, 2)

def compute_retention(m):
    """Retention score based on how recently mentor produced growth events."""
    data = mentor_stats.get(m)
    if not data or not data["history"]:
        return 0.0
    last_time = datetime.fromisoformat(data["history"][-1]["time"])
    days = (datetime.utcnow() - last_time).days
    score = max(0, 1 - (days / 30))  # decay after 30 days of inactivity
    return round(score, 2)

# ------------------------------------------------------------
# 🧭 REST Endpoints
# ------------------------------------------------------------
@router.get("/mentor/map")
async def mentor_map():
    return {"links": get_dynamic_pairs(), "timestamp": datetime.utcnow().isoformat()}

@router.get("/mentor/feed")
async def mentor_feed_endpoint():
    return {"feed": mentor_feed[-50:], "timestamp": datetime.utcnow().isoformat()}

@router.get("/mentor/analytics")
async def mentor_analytics():
    """Return summary metrics for all mentors."""
    analytics = []
    for m, data in mentor_stats.items():
        analytics.append(
            {
                "mentor": m,
                "total_growth": data["total_growth"],
                "sessions": data["sessions"],
                "unique_apprentices": len(data["apprentices"]),
                "efficiency_index": compute_efficiency(m),
                "retention_score": compute_retention(m),
            }
        )
    return {"analytics": analytics, "timestamp": datetime.utcnow().isoformat()}

@router.get("/mentor/history/{mentor_name}")
async def mentor_history(mentor_name: str):
    """Return detailed event history for a single mentor."""
    h = mentor_stats.get(mentor_name, {}).get("history", [])
    return {"mentor": mentor_name, "history": h[-50:]}

# ------------------------------------------------------------
# 🌐 WebSocket: Radar & Growth Pulses (analytics aware)
# ------------------------------------------------------------
@router.websocket("/ws/radar")
async def ws_radar(ws: WebSocket):
    await ws.accept()
    active_radars.add(ws)
    print("[Radar] Connection opened")

    try:
        while True:
            # Radar visualization data
            payload = random_radar_payload()
            await ws.send_text(json.dumps({"event": "radar_update", "payload": payload}))
            await asyncio.sleep(4)

            # Random growth event
            if random.random() < 0.3:
                pair = random.choice(get_dynamic_pairs())
                event = {
                    **pair,
                    "time": datetime.utcnow().isoformat(),
                    "event": "growth_pulse",
                }
                mentor_feed.append(event)
                update_mentor_stats(event)

                for c in list(active_radars):
                    await c.send_text(json.dumps({"event": "growth_pulse", "mentor": pair["mentor"], "time": event["time"]}))
    except WebSocketDisconnect:
        active_radars.remove(ws)
        print("[Radar] Connection closed")
