# ============================================================
# 🌱 Core4.AI – Seeder for core4ai_v53.db
# ------------------------------------------------------------
# Run once to populate your empty DB with 5 sample creators
# ============================================================

from main import Base, Creator, Wallet, calc_vis, calc_price, SessionLocal, engine
import random

# Recreate schema (if needed)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Only seed if empty
if db.query(Creator).count() == 0:
    print("Seeding database with creators...")
    creators = [
        ("Nova", "Fashion"),
        ("Rami", "Thinkers"),
        ("Sama", "Events"),
        ("Noor", "Humor"),
        ("Zayd", "Tech")
    ]

    for name, tribe in creators:
        vis = round(random.uniform(0.3, 0.9), 3)
        creator = Creator(
            name=name,
            tribe=tribe,
            vis_score=vis,
            token_price=calc_price(vis),
            followers=random.randint(1000, 10000)
        )
        db.add(creator)
        db.commit()

        wallet = Wallet(creator_id=creator.id, balance=random.uniform(50, 300))
        db.add(wallet)
        db.commit()

    print("✅ Done! core4ai_v53.db now has 5 creators.")
else:
    print("Database already seeded.")

db.close()
