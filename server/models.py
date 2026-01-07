from sqlalchemy import Column, Integer, String, Float, Text
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)  # "user" / "merchant" / "courier"
    shop_name = Column(String(100), nullable=True)
    balance = Column(Float, default=0.0)


class Dish(Base):
    __tablename__ = "dishes"
    id = Column(Integer, primary_key=True, index=True)
    merchant_id = Column(Integer, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    image_url = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    order_no = Column(String(32), unique=True, index=True, nullable=False)
    user_id = Column(Integer, index=True, nullable=False)
    merchant_id = Column(Integer, index=True, nullable=False)
    delivery_id = Column(Integer, index=True, nullable=True)  # 外卖员ID
    items = Column(Text, nullable=False)  # JSON: [{dish_id,name,quantity,price},...]
    total_price = Column(Float, nullable=False)
    status = Column(String(20), default="pending")  # pending / ready / delivering / done
