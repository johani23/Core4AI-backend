from fastapi import APIRouter

router = APIRouter(
    prefix="/buyer",
    tags=["Buyer"]
)

@router.get("/profile")
async def buyer_profile():
    return {"status": "ok", "endpoint": "buyer_profile"}

@router.get("/activity")
async def buyer_activity():
    return {"status": "ok", "endpoint": "buyer_activity"}

@router.get("/referrals")
async def buyer_referrals():
    return {"status": "ok", "endpoint": "buyer_referrals"}

@router.get("/influence")
async def buyer_influence():
    return {"status": "ok", "endpoint": "buyer_influence"}

@router.get("/transition")
async def buyer_transition():
    return {"status": "ok", "endpoint": "buyer_transition"}

@router.get("/rnd")
async def buyer_rnd():
    return {"status": "ok", "endpoint": "buyer_rnd"}
