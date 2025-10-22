from pydantic import BaseModel

class FlavorBase(BaseModel):
    name: str
    description: str | None = None
    price_per_slice: float

class FlavorCreate(FlavorBase):
    pass

class Flavor(FlavorBase):
    id: int
    tenant_id: int

    class Config:
        from_attributes = True
