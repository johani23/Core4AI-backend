# ---------------------------------------------------------------------
# 🧠 Core4.AI – Dopamine Intelligence Engine (MVP 19.10)
# ---------------------------------------------------------------------
# Provides unified endpoints for:
#   • Individual dopamine spikes & profiles
#   • Community & cluster heatmaps
#   • Temporal trend, forecast, and emotional weather
#
# Usage from main.py:
#   from modules.dopamine_engine import register_dopamine_routes
#   register_dopamine_routes(app, Base, SessionLocal)
# ---------------------------------------------------------------------

from fastapi import APIRouter, Depends, Query
from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime, timedelta
import random

# ---------------------------------------------------------------------
# Database Models
# ---------------------------------------------------------------------
Base = declarative_base()

class DopamineProfile(Base):
    __tablename__ = "dopamine_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, unique=True, index=True)
    current_level = Column(Float, default=50.0)
    baseline = Column(Float, default=50.0)
    streak = Column(Integer, default=0)
    last_peak_time = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DopamineEvent(Base):
    __tablename__ = "dopamine_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, index=True)
    action = Column(String)                       # e.g., "post", "vote"
    emotion_score = Column(Float, default=0.0)
    dopamine_value = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

# ---------------------------------------------------------------------
# Router Registration
# ---------------------------------------------------------------------
def register_dopamine_routes(app, Base, SessionLocal):

    router = APIRouter(prefix="/dopamine", tags=["Dopamine Engine"])

    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    # Ensure tables exist
    Base.metadata.create_all(bind=SessionLocal().bind)

    # --------------------------------------------------------------
    # 🧩 Individual Dopamine Event
    # --------------------------------------------------------------
    @router.post("/event")
    def dopamine_event(
        user_id: int = Query(...),
        action: str = Query("post"),
        emotion_score: float = Query(0.0),
        db: Session = Depends(get_db),
    ):
        """Record a dopamine spike for a user action."""
        profile = db.query(DopamineProfile).filter(DopamineProfile.user_id == user_id).first()
        if not profile:
            profile = DopamineProfile(user_id=user_id)
            db.add(profile)
            db.commit()
            db.refresh(profile)

        # Compute dopamine response
        base = 5.0
        action_boost = {"post": 3.0, "vote": 1.5, "comment": 2.0}.get(action, 1.0)
        randomness = random.uniform(0.5, 1.5)
        dopamine_value = round(base * action_boost * randomness * (1 + emotion_score / 2), 2)

        # Update profile level
        new_level = min(100.0, max(0.0, profile.current_level + dopamine_value / 3))
        profile.current_level = new_level
        profile.streak += 1
        profile.last_peak_time = datetime.utcnow()
        db.commit()

        # Log event
        event = DopamineEvent(
            user_id=user_id,
            action=action,
            emotion_score=emotion_score,
            dopamine_value=dopamine_value,
        )
        db.add(event)
        db.commit()

        return {
            "user_id": user_id,
            "action": action,
            "dopamine_value": dopamine_value,
            "current_level": profile.current_level,
            "timestamp": datetime.utcnow().isoformat(),
        }

    # --------------------------------------------------------------
    # 🔍 Get Single User Profile
    # --------------------------------------------------------------
    @router.get("/profile/{user_id}")
    def get_dopamine_profile(user_id: int, db: Session = Depends(get_db)):
        profile = db.query(DopamineProfile).filter(DopamineProfile.user_id == user_id).first()
        if not profile:
            profile = DopamineProfile(user_id=user_id)
            db.add(profile)
            db.commit()
            db.refresh(profile)

        decay = 0.98
        profile.current_level = round(profile.current_level * decay + profile.baseline * (1 - decay), 2)
        profile.updated_at = datetime.utcnow()
        db.commit()
        return profile

    # --------------------------------------------------------------
    # 🔥 Collective Heatmap
    # --------------------------------------------------------------
    @router.get("/heatmap")
    def get_collective_dopamine(db: Session = Depends(get_db)):
        profiles = db.query(DopamineProfile).all()
        if not profiles:
            return {"global_avg": 0, "total_users": 0, "heatmap": []}

        levels = [p.current_level for p in profiles]
        global_avg = round(sum(levels) / len(levels), 2)
        global_max, global_min = max(levels), min(levels)
        heatmap = []
        for p in profiles:
            norm = 0 if global_max == global_min else (p.current_level - global_min) / (global_max - global_min)
            heatmap.append({
                "user_id": p.user_id,
                "current_level": round(p.current_level, 2),
                "normalized": round(norm, 2),
                "streak": p.streak,
                "last_peak_time": p.last_peak_time,
            })
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "global_avg": global_avg,
            "max_level": global_max,
            "min_level": global_min,
            "total_users": len(profiles),
            "heatmap": sorted(heatmap, key=lambda x: x["current_level"], reverse=True),
        }

    # --------------------------------------------------------------
    # 🔗 Cluster Heatmap
    # --------------------------------------------------------------
    @router.get("/cluster-heatmap")
    def get_cluster_heatmap(db: Session = Depends(get_db)):
        profiles = db.query(DopamineProfile).all()
        if not profiles:
            return {"clusters": []}

        mock_clusters = {
            1: "Visionary Squad", 2: "Visionary Squad",
            3: "Neural Nomads",   4: "Neural Nomads",
            5: "Data Dreamers",   6: "Data Dreamers",
            7: "Fashionistas",    8: "Fashionistas",
        }

        cluster_data = {}
        for p in profiles:
            name = mock_clusters.get(p.user_id, "Unassigned")
            cluster_data.setdefault(name, []).append(p.current_level)

        clusters = [
            {"cluster": n, "avg_dopamine": round(sum(v)/len(v), 2), "members": len(v)}
            for n, v in cluster_data.items()
        ]
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "clusters": sorted(clusters, key=lambda x: x["avg_dopamine"], reverse=True)
        }

    # --------------------------------------------------------------
    # 🕒 Timeline
    # --------------------------------------------------------------
    @router.get("/timeline")
    def get_dopamine_timeline(hours: int = 24, db: Session = Depends(get_db)):
        now = datetime.utcnow()
        timeline = []
        for i in range(hours):
            t = now.replace(minute=0, second=0, microsecond=0) - timedelta(hours=i)
            level = random.uniform(45, 70)
            timeline.append({"timestamp": t.isoformat(), "avg_dopamine": round(level, 2)})
        timeline = list(reversed(timeline))
        avg = round(sum(x["avg_dopamine"] for x in timeline) / len(timeline), 2)
        return {"timestamp": now.isoformat(), "hours": hours, "global_avg": avg, "timeline": timeline}

    # --------------------------------------------------------------
    # 🔮 Forecast
    # --------------------------------------------------------------
    @router.get("/forecast")
    def get_dopamine_forecast(hours_ahead: int = 12, db: Session = Depends(get_db)):
        now = datetime.utcnow()
        past = [random.uniform(45, 70) for _ in range(24)]
        slope = (past[-1] - past[0]) / len(past)
        forecast = []
        last = past[-1]
        for i in range(1, hours_ahead + 1):
            drift = slope * i + random.uniform(-1.5, 1.5)
            next_val = max(40, min(100, last + drift))
            forecast.append({
                "timestamp": (now + timedelta(hours=i)).isoformat(),
                "predicted_dopamine": round(next_val, 2),
            })
            last = next_val
        avg_forecast = round(sum(f["predicted_dopamine"] for f in forecast) / len(forecast), 2)
        return {"timestamp": now.isoformat(), "hours_ahead": hours_ahead, "forecast_avg": avg_forecast, "forecast": forecast}

    # --------------------------------------------------------------
    # 🌦 Emotional Weather
    # --------------------------------------------------------------
    @router.get("/weather")
    def get_emotional_weather(db: Session = Depends(get_db)):
        heatmap = get_collective_dopamine(db)
        forecast = get_dopamine_forecast(db=db)
        avg_now = heatmap.get("global_avg", 50)
        avg_future = forecast.get("forecast_avg", 50)
        delta = avg_future - avg_now

        if delta > 3:
            trend = "rising"
        elif delta < -3:
            trend = "falling"
        else:
            trend = "stable"

        if avg_now >= 75:
            condition = "⚡ High creative euphoria"
        elif avg_now >= 60:
            condition = "🌤 Positive, inspired"
        elif avg_now >= 45:
            condition = "🌫 Moderate mood"
        else:
            condition = "🌧 Fatigued / low energy"

        forecast_msg = (
            "Momentum building, expect creative surge soon." if trend == "rising"
            else "Energy declining; consider reflective content." if trend == "falling"
            else "Stable mood balance across clusters."
        )

        risk = (
            "🔥 Over-stimulation risk" if avg_now > 85
            else "💤 Under-stimulation risk" if avg_now < 40
            else "✅ Balanced emotional state"
        )

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "current_avg": avg_now,
            "forecast_avg": avg_future,
            "trend": trend,
            "condition": condition,
            "forecast_message": forecast_msg,
            "emotional_risk": risk,
        }

    # --------------------------------------------------------------
    # Register router
    # --------------------------------------------------------------
    app.include_router(router)
