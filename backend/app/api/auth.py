from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(payload: LoginRequest):
    # MVP: não valida usuário, apenas retorna um token falso
    return {"token": "fake-jwt-for-testing"}
