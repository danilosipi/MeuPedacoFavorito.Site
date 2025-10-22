from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    tenant_id: int | None = None

class User(UserBase):
    id: int
    is_superadmin: bool
    tenant_id: int | None = None

    class Config:
        from_attributes = True
