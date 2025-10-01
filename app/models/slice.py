from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import SliceStatus

if TYPE_CHECKING:
    from app.models.order_item import OrderItem
    from app.models.pizza_batch import PizzaBatch
    from app.models.store import Store


class Slice(Base):
    __tablename__ = "slices"
    __table_args__ = (UniqueConstraint("batch_id", "sequence_number", name="uq_slices_batch_sequence"),)

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    store_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("stores.id", ondelete="CASCADE"), nullable=False)
    batch_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("pizza_batches.id", ondelete="CASCADE"), nullable=False)
    sequence_number: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[SliceStatus] = mapped_column(
        Enum(SliceStatus, name="slice_status", native_enum=False),
        nullable=False,
        default=SliceStatus.AVAILABLE,
        server_default=SliceStatus.AVAILABLE.value,
    )
    reserved_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    order_item_id: Mapped[UUID | None] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("order_items.id", ondelete="SET NULL"),
        nullable=True,
    )

    store: Mapped["Store"] = relationship(back_populates="slices")
    batch: Mapped["PizzaBatch"] = relationship(back_populates="slices")
    order_item: Mapped[Optional["OrderItem"]] = relationship(back_populates="slices")
