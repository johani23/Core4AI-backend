from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Tribe (Brand-Level)
class Tribe(BaseModel):
    tribe_id: str
    tribe_name: str
    brand: str
    leader_id: str
    created_at: datetime = datetime.utcnow()

# Tribe Member
class TribeMember(BaseModel):
    member_id: str
    tribe_id: str
    status: str  # active | pending | suspicious | kicked
    xp: int = 0
    joined_at: datetime = datetime.utcnow()

# Pending Reviews to validate membership
class PendingReview(BaseModel):
    review_id: str
    user_id: str
    product: str
    brand: str
    text: str
    sentiment: int
    authenticity_score: int
    tribe_id: str
