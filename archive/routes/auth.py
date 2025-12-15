from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# موديل بيانات المستخدم
class SignupRequest(BaseModel):
    username: str

# Signup (تسجيل مستخدم جديد)
@router.post("/signup")
async def signup(request: SignupRequest):
    return {"message": f"✅ User {request.username} signed up successfully"}
