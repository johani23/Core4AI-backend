from fastapi import APIRouter

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/emotion")
async def emotion_insights():
    return {"status": "ok", "endpoint": "analytics_emotion"}


@router.get("/stats")
async def unified_stats():
    return {"status": "ok", "endpoint": "analytics_stats"}


@router.get("/clusters")
async def cluster_stats():
    return {"status": "ok", "endpoint": "analytics_clusters"}
