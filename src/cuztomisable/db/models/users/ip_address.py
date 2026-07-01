import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from cuztomisable.db.base import Base


class UserIpAddress(Base):
    __tablename__ = "user_ip_addresses"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    deleted_by: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    ip_address: Mapped[str] = mapped_column(String(15))
    label: Mapped[Optional[str]] = mapped_column(String(), nullable=True)
    geo_label: Mapped[Optional[str]] = mapped_column(String(), nullable=True)
    latitude: Mapped[Optional[Decimal]] = mapped_column(Numeric(precision=10, scale=7), nullable=True)
    longitude: Mapped[Optional[Decimal]] = mapped_column(Numeric(precision=10, scale=7), nullable=True)
    fingerprint: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    last_used_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    remember: Mapped[bool] = mapped_column(Boolean, default=False)
    remember_until: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
