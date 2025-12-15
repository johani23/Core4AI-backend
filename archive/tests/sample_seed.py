# ============================================================
# 💎 Core4.AI – MVP-48 Sample Data Seeder
# ------------------------------------------------------------
# Creates 4 Core Tribes → 3 Sub-Tribes each → 3 Pods each (4 Members)
# Run once:  python sample_seed.py
# ============================================================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Base, CoreTribe, SubTribe, Pod, Member
import random

DATABASE_URL = "sqlite:///./core4ai_mvp48_unified.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# ------------------------------------------------------------
# 🏛️ Step 1: Define base data
# ------------------------------------------------------------
core_tribes_data = [
    ("🎨 Fashion", "F-Core", ["Streetwear", "Luxury & Design", "Beauty"]),
    ("🎭 Events", "E-Core", ["Concerts", "Sports", "Festivals"]),
    ("🧠 Thinkers", "T-Core", ["Philosophy", "TechTalks", "Psychology"]),
    ("😂 Humor", "H-Core", ["Sketch", "Memes", "Dark Humor"]),
]

# ------------------------------------------------------------
# 🌐 Step 2: Build hierarchy
# ------------------------------------------------------------
for core_name, symbol, sub_list in core_tribes_data:
    core = CoreTribe(
        name=core_name,
        symbol=symbol,
        token_value=random.uniform(80, 120),
        mood_index=random.uniform(40, 70),
    )
    session.add(core)
    session.commit()

    for sub_name in sub_list:
        sub = SubTribe(
            name=sub_name,
            core_tribe_id=core.id,
            heatflow_avg=random.uniform(0, 1),
        )
        session.add(sub)
        session.commit()

        # Create 3 Pods per sub-tribe
        for i in range(1, 4):
            pod = Pod(
                name=f"{sub_name} Pod {i}",
                sub_tribe_id=sub.id,
                heatflow_score=random.uniform(0, 100),
                qualification_status=random.choice(["pending", "qualified"]),
            )
            session.add(pod)
            session.commit()

            # Add 4 Members per Pod
            for j in range(1, 5):
                member = Member(
                    name=f"Member_{sub_name}_{i}_{j}",
                    role=random.choice(["creator", "strategist", "analyst", "leader"]),
                    score=random.uniform(50, 100),
                    pod_id=pod.id,
                )
                session.add(member)
            session.commit()

print("✅ Sample data inserted successfully into core4ai_mvp48_unified.db")
session.close()
