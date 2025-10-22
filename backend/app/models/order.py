from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base
import datetime

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    total_price = Column(Float, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    flavor_id = Column(Integer, ForeignKey("flavors.id"))
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False) # Price at the time of order
    order = relationship("Order", back_populates="items")
