from fastapi import FastAPI, Request, Depends
from app.api.routes import api
from app.core.tenants import get_tenant_from_request

app = FastAPI(title="Meu Pedaço Favorito - API")

@app.middleware("http")
async def tenant_context(request: Request, call_next):
    tenant = get_tenant_from_request(request)
    request.state.tenant = tenant
    response = await call_next(request)
    response.headers["X-Tenant-Processed"] = tenant
    return response

@app.get("/health")
async def health():
    return {"status": "ok"}

app.include_router(api, prefix="/api")
