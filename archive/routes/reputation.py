from fastapi import APIRouter

router = APIRouter()

points = {"value": 120}

@router.get("")
def get_reputation():
    return {"points": points["value"]}

@router.post("/increment")
def increment_reputation():
    points["value"] += 10
    return {"points": points["value"]}
