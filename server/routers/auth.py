from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import RegisterPayload, LoginPayload
from ..utils.auth import hash_password, verify_password, make_pseudo_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(payload: RegisterPayload, db: Session = Depends(get_db)):
    """注册用户 / 商家 / 外卖员"""
    role = payload.role.lower()
    if role not in ("user", "merchant", "courier"):
        return {"error": "用户类型应为 user / merchant / courier"}

    exists = db.query(User).filter(User.username == payload.username).first()
    if exists:
        return {"error": "用户名已存在"}

    u = User(
        username=payload.username,
        password_hash=hash_password(payload.password),
        role=role,
        shop_name=payload.shop_name if role == "merchant" else None,
        balance=0.0,
    )
    db.add(u)
    db.commit()
    db.refresh(u)

    return {"message": "注册成功", "user_id": u.id, "role": u.role}


@router.post("/login")
def login(payload: LoginPayload, db: Session = Depends(get_db)):
    """登录接口"""
    u = db.query(User).filter(User.username == payload.username).first()
    if not u or not verify_password(payload.password, u.password_hash):
        return {"error": "用户名或密码错误"}

    token = make_pseudo_token(u.id, u.role)
    return {
        "message": "登录成功",
        "token": token,
        "user_id": u.id,
        "role": u.role,
        "username": u.username,
        "shop_name": u.shop_name,
        "balance": u.balance,
    }
