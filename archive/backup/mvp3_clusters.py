from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict
import random
import uuid

router = APIRouter()

# ==============================
# 🟢 Models
# ==============================
class Member(BaseModel):
    id: str
    name: str
    role: str

class Team(BaseModel):
    id: str
    members: List[Member]

class TeamsResponse(BaseModel):
    teams: List[Team]

class TeamRequest(BaseModel):
    population: List[str]
    num_teams: int = 2

class VoteRequest(BaseModel):
    team_id: str
    idea_id: int

class VoteResponse(BaseModel):
    team_id: str
    idea_id: int
    votes: int

class SegmentContent(BaseModel):
    id: str
    segment: str
    text: str
    votes: int = 0

class SegmentsResponse(BaseModel):
    contents: List[SegmentContent]

# ==============================
# 🟢 In-memory DB
# ==============================
VOTES_DB: Dict[str, int] = {}

# ==============================
# 🟢 Roles
# ==============================
ROLES = [
    "Leader",
    "Analyst",
    "Connector",
    "Creative Thinker",
    "Humor Guy",
    "Event Organizer",
    "Fashion Voice",
    "Wildcard",
]

# ==============================
# 🟢 Segments
# ==============================
SEGMENTS = ["Fashion", "Humor", "Thinkers", "Event-goers"]

# ==============================
# 🟢 Endpoints
# ==============================

@router.post("/create_teams", response_model=TeamsResponse)
def api_create_teams(req: TeamRequest):
    random.shuffle(req.population)
    teams = []
    roles_pool = ROLES * ((len(req.population) // len(ROLES)) + 1)
    random.shuffle(roles_pool)

    for i in range(req.num_teams):
        team_members = []
        for name in req.population[i::req.num_teams]:
            member = Member(
                id=str(uuid.uuid4()),
                name=name,
                role=roles_pool.pop()
            )
            team_members.append(member)

        team = Team(id=f"team_{i+1}", members=team_members)
        teams.append(team)

    return TeamsResponse(teams=teams)


@router.post("/vote", response_model=VoteResponse)
def api_vote(req: VoteRequest):
    key = f"{req.team_id}_{req.idea_id}"
    if key not in VOTES_DB:
        VOTES_DB[key] = 0
    VOTES_DB[key] += 1
    return VoteResponse(team_id=req.team_id, idea_id=req.idea_id, votes=VOTES_DB[key])


@router.get("/segments", response_model=SegmentsResponse)
def api_get_segments():
    sample_texts = {
        "Fashion": ["Best outfit of the week 👗", "Top 3 style tips"],
        "Humor": ["Funniest meme 😂", "Best joke of the day"],
        "Thinkers": ["Deepest question 🤔", "Best book summary 📚"],
        "Event-goers": ["Top event highlights 🎉", "Best meetup idea"]
    }

    contents = []
    for seg in SEGMENTS:
        for txt in sample_texts[seg]:
            contents.append(
                SegmentContent(
                    id=str(uuid.uuid4()),
                    segment=seg,
                    text=txt,
                    votes=0
                )
            )

    return SegmentsResponse(contents=contents)
