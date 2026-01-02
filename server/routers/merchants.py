from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import User, Dish

router = APIRouter(prefix="/merchant", tags=["Merchants"])

@router.get("")
def list_merchants(db: Session = Depends(get_db)):
    merchants = db.query(User).filter(User.role == "merchant").all()
    return [{"id": m.id, "shop_name": m.shop_name or m.username} for m in merchants]

@router.get("/{merchant_id}/dishes", response_model=List[DishOut])
def get_dishes(merchant_id: int, db: Session = Depends(get_db)):
    dishes = db.query(Dish).filter(Dish.merchant_id == merchant_id).all()
    return dishes

@router.post("/add_dish")
def add_dish(payload: DishCreate, db: Session = Depends(get_db)):
    merchant = db.query(User).filter(User.id == payload.merchant_id, User.role == "merchant").first()
    if not merchant:
        return {"error": "商家不存在"}
    if payload.price < 0:
        return {"error": "价格不能为负"}

    d = Dish(
        merchant_id=payload.merchant_id,
        name=payload.name,
        price=payload.price,
        image_url=payload.image_url,
        description=payload.description
    )
    db.add(d)
    db.commit()
    db.refresh(d)
    return {"message": "添加成功", "dish_id": d.id}
