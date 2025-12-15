from fastapi import APIRouter

router = APIRouter(
    prefix="/creator",
    tags=["Creator"]
)

@router.get("/profile")
async def creator_profile():
    return {"status": "ok", "endpoint": "creator_profile"}

@router.get("/xp")
async def creator_xp():
    return {"status": "ok", "endpoint": "creator_xp"}

@router.get("/earnings")
async def creator_earnings():
    return {"status": "ok", "endpoint": "creator_earnings"}

@router.get("/autocreate")
async def creator_autocreate():
    return {"status": "ok", "endpoint": "creator_autocreate"}
