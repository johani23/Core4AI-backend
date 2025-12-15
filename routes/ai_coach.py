from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ContentRequest(BaseModel):
    text: str
    cluster: str = None

@router.post("/ai/coach")
def get_ai_tips(req: ContentRequest):
    tips = []
    if len(req.text) < 20:
        tips.append("🔹 Try writing a longer post to get more engagement.")
    if req.cluster == "fashion":
        tips.append("👗 Add an image to attract Fashion lovers.")
    if not tips:
        tips.append("✅ Looks good! Keep posting.")
    return {"tips": tips}
