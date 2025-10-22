from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .base import Base

class Flavor(Base):
    __tablename__ = "flavors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price_per_slice = Column(Float, nullable=False)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
