from pydantic import BaseModel
from datetime import datetime
from .catalog import Flavor

class OrderItemBase(BaseModel):
    flavor_id: int
    quantity: int

class OrderItem(OrderItemBase):
    id: int
    price: float

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    pass

class Order(OrderBase):
    id: int
    total_price: float
    status: str
    created_at: datetime
    items: list[OrderItem] = []

    class Config:
        from_attributes = True
