from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/dashboard")
async def client_dashboard(tenant: str, request: Request):
    return {"message": f"Dashboard for tenant {tenant}", "request_tenant": request.state.tenant}
