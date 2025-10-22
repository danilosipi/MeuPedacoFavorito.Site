from fastapi import APIRouter, Request
from pydantic import BaseModel, Field
from typing import List

router = APIRouter()

class CheckoutItem(BaseModel):
    id: int
    name: str
    price: float = Field(gt=0)
    qty: int = Field(default=1, gt=0)

class CheckoutIn(BaseModel):
    items: List[CheckoutItem]
    payment_method: str

@router.post("")
async def create_checkout(payload: CheckoutIn, request: Request):
    # MVP: simular cálculo/validação
    tenant = request.state.tenant
    total = sum(item.price * item.qty for item in payload.items)
    return {"tenant": tenant, "total": round(total, 2), "status": "pending"}
