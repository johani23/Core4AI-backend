from fastapi import APIRouter

router = APIRouter()

@router.get("")
def get_challenges():
    return [
        {"id": 1, "title": "Post your first meme", "points": 50},
        {"id": 2, "title": "Join a fashion trend", "points": 100},
    ]
