from pydantic import BaseModel
from typing import List

class CheckoutItem(BaseModel):
    id: int
    qty: int

class CheckoutIn(BaseModel):
    items: List[CheckoutItem]
    payment_method: str

class CheckoutOut(BaseModel):
    tenant: str
    total: float
    status: str
