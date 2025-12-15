from fastapi import APIRouter

router = APIRouter()

@router.get("/spotlight")
def get_spotlight():
    # لاحقًا: احسب النمو الأسرع من DB
    user = {
        "name": "Sama",
        "bio": "Loves fashion & events 🎉",
        "avatar": "/avatars/sama.png",
        "followers": 1234
    }
    return {"spotlight": user}
