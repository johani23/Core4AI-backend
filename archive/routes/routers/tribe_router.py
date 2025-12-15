from fastapi import APIRouter
from models.tribe_models import Tribe, TribeMember, PendingReview

router = APIRouter()

TRIBES = {}
TRIBE_MEMBERS = {}
PENDING_REVIEWS = {}

# --------------------------------------------------------------------
# 1) Create Tribe (Brand-Level)
# --------------------------------------------------------------------
@router.post("/create-tribe")
def create_tribe(data: Tribe):
    TRIBES[data.tribe_id] = data
    TRIBE_MEMBERS[data.tribe_id] = []
    return {"status": "success", "data": data}

# --------------------------------------------------------------------
# 2) Membership check (called when user submits review)
# --------------------------------------------------------------------
@router.post("/evaluate-membership")
def evaluate_membership(review: PendingReview):
    PENDING_REVIEWS[review.review_id] = review

    return {
        "status": "pending_review",
        "review_id": review.review_id,
        "tribe_id": review.tribe_id,
        "brand": review.brand,
        "sentiment": review.sentiment,
    }

# --------------------------------------------------------------------
# 3) Approve / Reject membership by tribe leader
# --------------------------------------------------------------------
@router.post("/verify-review")
def verify_review(data: dict):
    review_id = data["review_id"]
    action = data["action"]

    review = PENDING_REVIEWS.get(review_id)

    if not review:
        return {"error": "Review not found"}

    if action == "approve":
        TRIBE_MEMBERS[review.tribe_id].append(TribeMember(
            member_id=review.user_id,
            tribe_id=review.tribe_id,
            status="active",
            xp=10
        ))
        del PENDING_REVIEWS[review_id]
        return {"status": "member_added", "user": review.user_id}

    if action == "reject":
        del PENDING_REVIEWS[review_id]
        return {"status": "rejected"}

    if action == "merchant_check":
        return {"status": "sent_to_merchant", "review_id": review_id}

    return {"error": "invalid action"}

# --------------------------------------------------------------------
# 4) Get Member List
# --------------------------------------------------------------------
@router.get("/members/{tribe_id}")
def get_members(tribe_id: str):
    return {"members": TRIBE_MEMBERS.get(tribe_id, [])}

# --------------------------------------------------------------------
# 5) Handle member actions (kick, flag, promote)
# --------------------------------------------------------------------
@router.post("/member-action")
def member_action(data: dict):
    tribe_id = data["tribe_id"]
    member_id = data["member_id"]
    action = data["action"]

    members = TRIBE_MEMBERS.get(tribe_id, [])

    for m in members:
        if m.member_id == member_id:

            if action == "kick":
                m.status = "kicked"

            elif action == "flag":
                m.status = "suspicious"

            elif action == "approve":
                m.status = "active"

            elif action == "promote":
                m.status = "subtribe_leader"

            return {"status": "updated", "member": m}

    return {"error": "member not found"}
