from fastapi import APIRouter
from services.data_sync import get_unified_stats

router = APIRouter()

@router.get("/unified-stats")
def unified_stats():
    stats = get_unified_stats()
    return {"status": "ok", "data": stats}
