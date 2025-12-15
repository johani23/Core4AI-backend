from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import models, database

router = APIRouter(prefix="/economy", tags=["Economy"])

@router.post("/add_coins")
def add_coins(user_id: int, amount: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return {"error": "User not found"}
    user.coins += amount
    db.add(models.Transaction(user_id=user_id, amount=amount))
    db.commit()
    db.refresh(user)
    return {"user_id": user.id, "coins": user.coins}

@router.post("/spend_coins")
def spend_coins(user_id: int, amount: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return {"error": "User not found"}
    if user.coins < amount:
        return {"error": "Not enough coins"}
    user.coins -= amount
    db.add(models.Transaction(user_id=user_id, amount=-amount))
    db.commit()
    db.refresh(user)
    return {"user_id": user.id, "coins": user.coins}

@router.get("/wallet/{user_id}")
def get_wallet(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return {"error": "User not found"}
    return {"user_id": user.id, "coins": user.coins}

@router.get("/transactions/{user_id}")
def list_transactions(user_id: int, db: Session = Depends(database.get_db)):
    txs = db.query(models.Transaction).filter(models.Transaction.user_id == user_id).all()
    return [{"id": t.id, "amount": t.amount, "created_at": t.created_at} for t in txs]
