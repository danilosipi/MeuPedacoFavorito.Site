from pydantic import BaseModel

class TenantBase(BaseModel):
    name: str
    slug: str

class TenantCreate(TenantBase):
    pass

class Tenant(TenantBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
