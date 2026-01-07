from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Order, User
import json

router = APIRouter(prefix="/courier", tags=["Couriers"])

# 获取所有可接单（ready）的订单
@router.get("/available")
def get_available_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.status == "ready").order_by(Order.id.desc()).all()
    result = []
    for o in orders:
        u = db.query(User).filter(User.id == o.user_id).first()
        m = db.query(User).filter(User.id == o.merchant_id).first()
        result.append({
            "order_no": o.order_no,
            "user": u.username if u else "未知",
            "merchant": m.shop_name if m and m.shop_name else "未命名商家",
            "items": json.loads(o.items),
            "total_price": o.total_price,
            "status": o.status
        })
    return result


# 接单
@router.put("/accept/{order_no}/{courier_id}")
def accept_order(order_no: str, courier_id: int, db: Session = Depends(get_db)):
    o = db.query(Order).filter(Order.order_no == order_no).first()
    if not o:
        return {"error": "订单不存在"}
    if o.status != "ready":
        return {"error": "订单状态错误，无法接单"}
    courier = db.query(User).filter(User.id == courier_id, User.role == "courier").first()
    if not courier:
        return {"error": "配送员不存在"}
    o.delivery_id = courier_id
    o.status = "delivering"
    db.commit()
    return {"message": "已成功接单"}


# 查看我的配送单
@router.get("/my/{courier_id}")
def get_my_orders(courier_id: int, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.delivery_id == courier_id).order_by(Order.id.desc()).all()
    result = []
    for o in orders:
        m = db.query(User).filter(User.id == o.merchant_id).first()
        result.append({
            "order_no": o.order_no,
            "merchant": m.shop_name if m else "未知商家",
            "items": json.loads(o.items),
            "total_price": o.total_price,
            "status": o.status
        })
    return result


# 配送完成
@router.put("/deliver/{order_no}")
def mark_delivered(order_no: str, db: Session = Depends(get_db)):
    o = db.query(Order).filter(Order.order_no == order_no).first()
    if not o:
        return {"error": "订单不存在"}
    if o.status != "delivering":
        return {"error": "当前状态无法标记为已送达"}
    o.status = "done"
    db.commit()
    return {"message": "配送完成"}
