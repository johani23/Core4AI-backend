from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# موديل المنشور
class PostRequest(BaseModel):
    user_id: int
    content: str

# قاعدة بيانات وهمية
posts = []

# جلب كل المنشورات
@router.get("/")
async def get_posts():
    return posts

# إضافة منشور جديد
@router.post("/")
async def add_post(post: PostRequest):
    new_post = {"id": len(posts) + 1, "user_id": post.user_id, "content": post.content, "upvotes": 0}
    posts.append(new_post)
    return new_post

# Upvote
@router.post("/{post_id}/upvote")
async def upvote_post(post_id: int):
    for post in posts:
        if post["id"] == post_id:
            post["upvotes"] += 1
            return {"message": "Post upvoted", "post": post}
    return {"error": "Post not found"}
