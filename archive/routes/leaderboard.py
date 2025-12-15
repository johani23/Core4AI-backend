from fastapi import APIRouter

router = APIRouter()

@router.get("")
def get_leaderboard():
    return {
        "week": [
            {"name": "Noor", "points": 220},
            {"name": "Sama", "points": 120},
        ],
        "month": [
            {"name": "Noor", "points": 400},
            {"name": "Sama", "points": 200},
        ],
        "risingStars": [
            {"name": "Loulia", "growth": 80},
            {"name": "Saba", "growth": 50},
        ]
    }
