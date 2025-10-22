from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/dashboard")
async def admin_dashboard(request: Request):
    return {"message": "Welcome to the Superadmin Dashboard", "tenant": request.state.tenant}
