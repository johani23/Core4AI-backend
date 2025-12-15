# ============================================================================
# 🎬 Core4.AI – Creator API (Feed + Create Post)
# ============================================================================

from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

router = APIRouter(
    prefix="/api/creator",
    tags=["creator"]
)

class CreatorPost(BaseModel):
    text: str
    image: Optional[str] = None
    creator_id: Optional[str] = "demo-creator"

CREATOR_FEED = []

@router.get("/feed")
async def get_feed():
    return CREATOR_FEED

@router.post("/post")
async def create_post(post: CreatorPost):
    new_post = {
        "id": len(CREATOR_FEED) + 1,
        "creator_id": post.creator_id,
        "text": post.text,
        "image": post.image,
        "timestamp": datetime.now().isoformat()
    }
    CREATOR_FEED.append(new_post)
    return {"status": "success", "post": new_post}

@router.get("/stats")
async def stats():
    return {
        "posts": len(CREATOR_FEED),
        "last_post": CREATOR_FEED[-1] if CREATOR_FEED else None
    }
