from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Order, User
from ..schemas import OrderCreate
import json
from datetime import datetime

router = APIRouter(prefix="/order", tags=["Orders"])


# ---------- 创建订单 ----------
@router.post("/create")
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == payload.user_id, User.role == "user").first()
    merchant = db.query(User).filter(User.id == payload.merchant_id, User.role == "merchant").first()
    if not user or not merchant:
        return {"error": "用户或商家不存在"}

    total_price = 0.0
    for item in payload.items:
        if item.quantity <= 0:
            return {"error": "数量需大于 0"}
        total_price += item.price * item.quantity

    if user.balance < total_price:
        return {"error": "余额不足，请充值"}

    user.balance -= total_price

    today_str = datetime.now().strftime("%Y%m%d")
    merchant_id = payload.merchant_id

    today_orders = (
        db.query(Order)
        .filter(Order.merchant_id == merchant_id, Order.order_no.like(f"{today_str}-M{merchant_id}-%"))
        .order_by(Order.order_no.desc())
        .all()
    )

    next_num = 1
    if today_orders:
        last_order_no = today_orders[0].order_no
        last_num = int(last_order_no.split("-")[-1])
        next_num = last_num + 1

    order_no = f"{today_str}-M{merchant_id}-{next_num:03d}"

    order = Order(
        order_no=order_no,
        user_id=payload.user_id,
        merchant_id=payload.merchant_id,
        items=json.dumps([i.model_dump() for i in payload.items], ensure_ascii=False),
        total_price=total_price,
        status="pending",
        delivery_id=None
    )
    db.add(order)
    db.commit()

    return {
        "message": "下单成功",
        "order_no": order_no,
        "total_price": total_price,
        "remain_balance": user.balance
    }


# ---------- 商家查看订单 ----------
@router.get("/merchant/{merchant_id}")
def get_merchant_orders(merchant_id: int, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.merchant_id == merchant_id).order_by(Order.id.desc()).all()
    result = []
    for o in orders:
        u = db.query(User).filter(User.id == o.user_id).first()
        merchant = db.query(User).filter(User.id == o.merchant_id).first()
        courier = db.query(User).filter(User.id == o.delivery_id).first() if o.delivery_id else None
        result.append({
            "order_no": o.order_no,
            "user": u.username if u else "未知",
            "merchant_name": merchant.shop_name if merchant and merchant.shop_name else "未命名商家",
            "deliveryman": courier.username if courier else None,
            "items": json.loads(o.items),
            "total_price": o.total_price,
            "status": o.status
        })
    return result


# ---------- 用户查看订单 ----------
@router.get("/user/{user_id}")
def get_user_orders(user_id: int, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.user_id == user_id).order_by(Order.id.desc()).all()
    result = []
    for o in orders:
        merchant = db.query(User).filter(User.id == o.merchant_id).first()
        courier = db.query(User).filter(User.id == o.delivery_id).first() if o.delivery_id else None
        result.append({
            "order_no": o.order_no,
            "merchant_id": o.merchant_id,
            "merchant_name": merchant.shop_name if merchant and merchant.shop_name else "未命名商家",
            "deliveryman": courier.username if courier else "未分配",
            "items": json.loads(o.items),
            "total_price": o.total_price,
            "status": o.status
        })
    return result


# ---------- 商家标记菜品制作完成 ----------
@router.put("/{order_no}/ready")
def mark_ready(order_no: str, db: Session = Depends(get_db)):
    o = db.query(Order).filter(Order.order_no == order_no).first()
    if not o:
        return {"error": "订单不存在"}
    if o.status != "pending":
        return {"error": "订单状态错误，无法标记完成"}
    o.status = "ready"
    db.commit()
    return {"message": "菜品制作完成，等待配送员接单"}


# ---------- 外卖员查看可接订单 ----------
@router.get("/available")
def get_available_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.status == "ready").order_by(Order.id.desc()).all()
    result = []
    for o in orders:
        merchant = db.query(User).filter(User.id == o.merchant_id).first()
        result.append({
            "order_no": o.order_no,
            "merchant_name": merchant.shop_name if merchant else "未知",
            "total_price": o.total_price,
            "status": o.status
        })
    return result


# ---------- 外卖员接单 ----------
@router.put("/{order_no}/assign/{courier_id}")
def assign_courier(order_no: str, courier_id: int, db: Session = Depends(get_db)):
    o = db.query(Order).filter(Order.order_no == order_no).first()
    if not o:
        return {"error": "订单不存在"}
    if o.status != "ready":
        return {"error": "当前订单不可接"}
    courier = db.query(User).filter(User.id == courier_id, User.role == "courier").first()
    if not courier:
        return {"error": "配送员不存在"}

    o.delivery_id = courier_id
    o.status = "delivering"
    db.commit()
    return {"message": f"配送员 {courier.username} 已接单"}


# ---------- 外卖员查看自己订单 ----------
@router.get("/courier/{courier_id}")
def get_courier_orders(courier_id: int, db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.delivery_id == courier_id).order_by(Order.id.desc()).all()
    result = []
    for o in orders:
        merchant = db.query(User).filter(User.id == o.merchant_id).first()
        result.append({
            "order_no": o.order_no,
            "merchant_name": merchant.shop_name if merchant else "未知",
            "total_price": o.total_price,
            "status": o.status
        })
    return result


# ---------- 外卖员标记送达 ----------
@router.put("/{order_no}/delivered")
def mark_delivered(order_no: str, db: Session = Depends(get_db)):
    o = db.query(Order).filter(Order.order_no == order_no).first()
    if not o:
        return {"error": "订单不存在"}
    if o.status != "delivering":
        return {"error": "状态错误，无法标记送达"}
    o.status = "done"
    db.commit()
    return {"message": "订单已送达，交易完成"}
