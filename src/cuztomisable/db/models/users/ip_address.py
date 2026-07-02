import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cuztomisable.db.base import Base, SoftDeleteMixin, TimestampMixin


class UserIpAddress(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "user_ip_addresses"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
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

    user: Mapped["User"] = relationship("User", foreign_keys=[user_id])
