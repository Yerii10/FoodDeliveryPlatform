from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User

router = APIRouter(prefix="/user", tags=["Users"])

@router.get("/{user_id}/balance")
def get_balance(user_id: int, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.id == user_id).first()
    if not u:
        return {"error": "用户不存在"}
    return {"balance": u.balance}

@router.put("/{user_id}/deposit")
def deposit_balance(user_id: int, amount: float, db: Session = Depends(get_db)):
    if amount <= 0:
        return {"error": "充值金额需大于 0"}
    u = db.query(User).filter(User.id == user_id).first()
    if not u:
        return {"error": "用户不存在"}
    u.balance += amount
    db.commit()
    return {"message": "充值成功", "balance": u.balance}
