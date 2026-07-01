import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from cuztomisable.db.base import Base


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    deleted_by: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    address: Mapped[Optional[str]] = mapped_column(String(), nullable=True)
    address_two: Mapped[Optional[str]] = mapped_column(String(), nullable=True)
    address_three: Mapped[Optional[str]] = mapped_column(String(), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    state_or_province: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    zip_or_postal_code: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    is_default: Mapped[bool] = mapped_column('default', Boolean, default=False)
    shipping: Mapped[bool] = mapped_column(Boolean, default=False)
    billing: Mapped[bool] = mapped_column(Boolean, default=False)
