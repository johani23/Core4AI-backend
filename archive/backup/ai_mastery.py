import random
from .models import Tribe, Creator

def analyze_clip(filename: str) -> int:
    """Mock AI scoring; later connect to real ML model."""
    return random.randint(20, 95)

def assign_level(score: int) -> str:
    if score < 40:
        return "Rising Voice"
    elif score < 65:
        return "Emerging Influencer"
    elif score < 85:
        return "Core Creator"
    else:
        return "Mentor"

def auto_assign_tribe(db, creator_name: str, level: str):
    """Assign creator to tribe with closest average mastery."""
    tribe = db.query(Tribe).order_by(Tribe.avg_mastery.asc()).first()
    if not tribe:
        return None
    creator = db.query(Creator).filter_by(name=creator_name).first()
    if creator:
        creator.tribe_id = tribe.id
        creator.level = level
        db.commit()
    return tribe
