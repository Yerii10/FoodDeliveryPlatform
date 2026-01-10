from pydantic import BaseModel, Field
from typing import List, Optional

class RegisterPayload(BaseModel):
    username: str
    password: str
    role: str  # "user" or "merchant"
    shop_name: Optional[str] = None

class LoginPayload(BaseModel):
    username: str
    password: str

class DishCreate(BaseModel):
    merchant_id: int
    name: str
    price: float
    image_url: Optional[str] = None
    description: Optional[str] = None

class DishOut(BaseModel):
    id: int
    merchant_id: int
    name: str
    price: float
    image_url: Optional[str] = None
    description: Optional[str] = None
    class Config:
        from_attributes = True

class OrderItem(BaseModel):
    dish_id: int
    name: str
    quantity: int = Field(ge=1)
    price: float

class OrderCreate(BaseModel):
    user_id: int
    merchant_id: int
    items: List[OrderItem]

class OrderOut(BaseModel):
    order_no: str
    user: str
    items: List[OrderItem]
    total_price: float
    status: str
