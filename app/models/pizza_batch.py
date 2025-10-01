from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import BatchStatus

if TYPE_CHECKING:
    from app.models.menu_item import MenuItem
    from app.models.slice import Slice
    from app.models.store import Store


class PizzaBatch(Base):
    __tablename__ = "pizza_batches"
    __table_args__ = (UniqueConstraint("store_id", "reference", name="uq_pizza_batches_store_reference"),)

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    store_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("stores.id", ondelete="CASCADE"), nullable=False)
    menu_item_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("menu_items.id", ondelete="RESTRICT"), nullable=False)
    reference: Mapped[str] = mapped_column(String(64), nullable=False)
    total_slices: Mapped[int] = mapped_column(Integer, nullable=False)
    opened_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[BatchStatus] = mapped_column(
        Enum(BatchStatus, name="batch_status", native_enum=False),
        nullable=False,
        default=BatchStatus.OPEN,
        server_default=BatchStatus.OPEN.value,
    )

    store: Mapped["Store"] = relationship(back_populates="pizza_batches")
    menu_item: Mapped["MenuItem"] = relationship(back_populates="pizza_batches")
    slices: Mapped[list["Slice"]] = relationship(back_populates="batch", cascade="all, delete-orphan")
