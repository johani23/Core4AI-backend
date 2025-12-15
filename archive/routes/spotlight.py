from fastapi import APIRouter

router = APIRouter()

@router.get("")
def get_spotlight():
    return {
        "name": "Sama",
        "bio": "Loves fashion & events 🎉",
        "avatar": "/avatars/sama.png",
        "followers": 1234,
    }
