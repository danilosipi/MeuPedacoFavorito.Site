from fastapi import APIRouter

from .admin import router as admin_router
from .client import router as client_router
from .public import router as public_router
from .checkout import router as checkout_router
from .orders import router as orders_router
from .auth import router as auth_router

api = APIRouter()
api.include_router(admin_router, prefix="/admin", tags=["admin"])
api.include_router(client_router, prefix="/client/{tenant}", tags=["client"])
api.include_router(public_router, prefix="/public/{tenant}", tags=["public"])
api.include_router(checkout_router, prefix="/checkout", tags=["checkout"])
api.include_router(orders_router, prefix="/orders", tags=["orders"])
api.include_router(auth_router, prefix="/auth", tags=["auth"])
