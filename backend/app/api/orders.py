from fastapi import APIRouter, Request

router = APIRouter()

@router.get("")
async def list_orders(request: Request):
    return {"tenant": request.state.tenant, "data": []}
