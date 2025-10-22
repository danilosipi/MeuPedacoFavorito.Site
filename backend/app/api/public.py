from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/catalog")
async def public_catalog(tenant: str, request: Request):
    return {"message": f"Public catalog for tenant {tenant}", "request_tenant": request.state.tenant, "items": []}
