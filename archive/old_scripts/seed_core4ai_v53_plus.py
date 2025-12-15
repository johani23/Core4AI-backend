# ============================================================
# 💎 Core4.AI – Dynamic Seeder v53+
# ------------------------------------------------------------
# Populates creators, wallets, and live-impact transactions.
# Every transaction adjusts VIS, token price, and balances.
# ============================================================

from main import Base, Creator, Wallet, Transaction, calc_vis, calc_price, SessionLocal, engine
from datetime import datetime, timedelta
import random

# --- Initialize DB ---
Base.metadata.create_all(bind=engine)
db = SessionLocal()

# ------------------------------------------------------------
# 🧩 Step 1: Seed Creators + Wallets
# ------------------------------------------------------------
if db.query(Creator).count() == 0:
    print("🌱 Creating sample creators and wallets...")
    creators_data = [
        ("Nova", "Fashion"),
        ("Rami", "Thinkers"),
        ("Sama", "Events"),
        ("Noor", "Humor"),
        ("Zayd", "Tech"),
    ]

    for name, tribe in creators_data:
        vis = round(random.uniform(0.45, 0.85), 3)
        creator = Creator(
            name=name,
            tribe=tribe,
            vis_score=vis,
            token_price=calc_price(vis),
            followers=random.randint(1000, 10000),
        )
        db.add(creator)
        db.commit()

        wallet = Wallet(creator_id=creator.id, balance=random.uniform(200, 500))
        db.add(wallet)
        db.commit()
    print("✅ 5 creators + wallets added.")
else:
    print("⚠️ Creators already exist, skipping...")

# ------------------------------------------------------------
# 💸 Step 2: Dynamic Transactions Simulation
# ------------------------------------------------------------
if db.query(Transaction).count() == 0:
    print("💫 Seeding transactions with live balance + VIS impact...")

    creators = db.query(Creator).all()
    wallets = {w.creator_id: w for w in db.query(Wallet).all()}

    for _ in range(20):
        sender, receiver = random.sample(creators, 2)
        amount = round(random.uniform(10, 60), 2)

        sender_wallet = wallets[sender.id]
        receiver_wallet = wallets[receiver.id]

        # Skip if sender has low balance
        if sender_wallet.balance < amount:
            continue

        # Update balances
        sender_wallet.balance -= amount
        receiver_wallet.balance += amount

        # VIS adjustment ±1–3%
        vis_delta = random.uniform(0.01, 0.03)
        sender.vis_score = max(0.3, sender.vis_score * (1 - vis_delta))
        receiver.vis_score = min(0.95, receiver.vis_score * (1 + vis_delta))

        # Recalculate token prices
        sender.token_price = calc_price(sender.vis_score)
        receiver.token_price = calc_price(receiver.vis_score)

        # Log transaction
        tx = Transaction(
            sender=sender.name,
            receiver=receiver.name,
            amount=amount,
            type=random.choice(["vote_reward", "trade", "gift"]),
            timestamp=datetime.utcnow() - timedelta(minutes=random.randint(5, 1200)),
        )
        db.add(tx)
        db.commit()

    print("✅ Transactions created & VIS dynamics updated.")
else:
    print("⚠️ Transactions already exist, skipping...")

# ------------------------------------------------------------
# 📊 Step 3: Summary Output
# ------------------------------------------------------------
creators = db.query(Creator).all()
print("\n📈 Final Creator Stats:")
for c in creators:
    w = db.query(Wallet).filter_by(creator_id=c.id).first()
    print(
        f" - {c.name:<6} | Tribe: {c.tribe:<10} | VIS: {c.vis_score:.3f} | "
        f"Token: {c.token_price:.2f} | Balance: {w.balance:.1f}"
    )

db.close()
print("\n🎯 core4ai_v53.db successfully populated with dynamic economy data.")
