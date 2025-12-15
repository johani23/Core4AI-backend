from fastapi import APIRouter

router = APIRouter(
    prefix="/system",
    tags=["System"]
)

@router.get("/auth")
async def system_auth():
    return {"status": "ok", "endpoint": "system_auth"}

@router.get("/user")
async def system_user():
    return {"status": "ok", "endpoint": "system_user"}

@router.get("/posts")
async def system_posts():
    return {"status": "ok", "endpoint": "system_posts"}

@router.get("/economy")
async def system_economy():
    return {"status": "ok", "endpoint": "system_economy"}
