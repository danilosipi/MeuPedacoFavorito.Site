from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Boolean, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.menu_item import MenuItem
    from app.models.order import Order
    from app.models.pizza_batch import PizzaBatch
    from app.models.slice import Slice


class Store(Base):
    __tablename__ = "stores"
    __table_args__ = (UniqueConstraint("slug", name="uq_stores_slug"),)

    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    slug: Mapped[str] = mapped_column(String(150), nullable=False)
    timezone: Mapped[str] = mapped_column(String(64), nullable=False, default="America/Sao_Paulo")
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    menu_items: Mapped[list["MenuItem"]] = relationship(back_populates="store", cascade="all, delete-orphan")
    pizza_batches: Mapped[list["PizzaBatch"]] = relationship(back_populates="store", cascade="all, delete-orphan")
    orders: Mapped[list["Order"]] = relationship(back_populates="store", cascade="all, delete-orphan")
    slices: Mapped[list["Slice"]] = relationship(back_populates="store", cascade="all, delete-orphan")
