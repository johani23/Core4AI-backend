# ============================================================
# 💎 Core4.AI – routers/subtribe.py (v167 Add-on “Closed Sub-Tribes”)
# ------------------------------------------------------------
# • Creates & manages sub-tribes per campaign
# • Invites, joins, and stats retrieval
# • Works independently of AI core logic
# ============================================================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid, logging

router = APIRouter()
logger = logging.getLogger("core4ai")

# in-memory stores for beta
subtribes = {}
invites = {}

# ------------------------------------------------------------
# Schemas
# ------------------------------------------------------------
class SubTribeCreate(BaseModel):
    leader_id: str
    campaign_id: str
    name: str
    commission_split: float = 0.15

class SubTribeInvite(BaseModel):
    subtribe_id: str
    invitee_id: str

class SubTribeJoin(BaseModel):
    subtribe_id: str
    user_id: str

# ------------------------------------------------------------
# Endpoints
# ------------------------------------------------------------
@router.post("/subtribe/create")
def create_subtribe(data: SubTribeCreate):
    sid = str(uuid.uuid4())
    subtribes[sid] = {
        "id": sid,
        "leader_id": data.leader_id,
        "campaign_id": data.campaign_id,
        "name": data.name,
        "commission_split": data.commission_split,
        "members": [data.leader_id],
        "stats": {"sales": 0, "tokens": 0},
    }
    logger.info(f"🪶 Sub-Tribe created: {data.name}")
    return {"subtribe_id": sid, "status": "created"}

@router.post("/subtribe/invite")
def invite_member(data: SubTribeInvite):
    if data.subtribe_id not in subtribes:
        raise HTTPException(status_code=404, detail="Sub-tribe not found")
    invites.setdefault(data.subtribe_id, []).append(data.invitee_id)
    return {"status": "invited", "invitee": data.invitee_id}

@router.post("/subtribe/join")
def join_subtribe(data: SubTribeJoin):
    if data.subtribe_id not in subtribes:
        raise HTTPException(status_code=404, detail="Sub-tribe not found")
    if data.user_id in subtribes[data.subtribe_id]["members"]:
        return {"status": "already member"}
    subtribes[data.subtribe_id]["members"].append(data.user_id)
    return {"status": "joined", "members": subtribes[data.subtribe_id]["members"]}

@router.get("/subtribe/stats")
def get_subtribe_stats(subtribe_id: str):
    if subtribe_id not in subtribes:
        raise HTTPException(status_code=404, detail="Sub-tribe not found")
    return subtribes[subtribe_id]
