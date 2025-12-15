# ============================================================
# 💎 Core4.AI – Integration Bridge (v53.5 → v60)
# ------------------------------------------------------------
# ✅ Aggregates Creator, Tribe, Wallet, Arena data
# ✅ Generates unified JSON for MVP-60 Frontend
# ✅ Acts as transitional adapter between economy & analytics layers
# ============================================================

from fastapi import Depends
from sqlalchemy import func
from typing import Dict, Any
from main import app, get_db, Creator, Wallet, AIArenaMatch, calc_vis, calc_price
from sqlalchemy.orm import Session
import random

# ------------------------------------------------------------
# 🧩 Helper: Tribe Mood Calculation
# ------------------------------------------------------------
def compute_tribe_mood(db: Session) -> list[Dict[str, Any]]:
    tribes = db.query(Creator.tribe, func.avg(Creator.vis_score)).group_by(Creator.tribe).all()
    mood_data = []
    for tribe, avg_vis in tribes:
        mood_index = round(avg_vis * 100 + random.uniform(-5, 5), 2)
        mood_data.append({
            "name": tribe,
            "mood_index": max(0, min(100, mood_index))
        })
    return mood_data

# ------------------------------------------------------------
# 🧩 Helper: Global Indicators
# ------------------------------------------------------------
def compute_global_indicators(db: Session):
    total_creators = db.query(Creator).count()
    total_wallets = db.query(Wallet).count()
    total_matches = db.query(AIArenaMatch).count()
    avg_vis = db.query(func.avg(Creator.vis_score)).scalar() or 0
    avg_price = db.query(func.avg(Creator.token_price)).scalar() or 0
    return {
        "total_creators": total_creators,
        "total_wallets": total_wallets,
        "total_matches": total_matches,
        "avg_vis": round(avg_vis, 2),
        "avg_price": round(avg_price, 2),
    }

# ------------------------------------------------------------
# 🌉 Unified Bridge Endpoint
# ------------------------------------------------------------
@app.get("/api/bridge")
def unified_bridge(db: Session = Depends(get_db)):
    # 💎 Creators overview
    creators = [
        {
            "name": c.name,
            "tribe": c.tribe,
            "vis": c.vis_score,
            "price": c.token_price,
            "followers": c.followers,
        }
        for c in db.query(Creator).limit(10).all()
    ]

    # 🌍 Tribe mood
    tribe_mood = compute_tribe_mood(db)

    # ⚙️ Global indicators
    global_stats = compute_global_indicators(db)

    # 🧠 AI Arena summary
    arena_summary = {
        "matches": db.query(AIArenaMatch).count(),
        "avg_confidence": round(db.query(func.avg(AIArenaMatch.confidence)).scalar() or 0, 2),
    }

    return {
        "status": "bridge_active",
        "global": global_stats,
        "tribes": tribe_mood,
        "creators": creators,
        "arena": arena_summary,
    }
