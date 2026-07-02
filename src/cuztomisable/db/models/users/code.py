import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cuztomisable.db.base import Base, SoftDeleteMixin, TimestampMixin


class UserCode(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "user_codes"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    user_ip_address_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("user_ip_addresses.id", ondelete="SET NULL"), nullable=True)
    code: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    token: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    used_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    sent_via: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)
    attempt_counter: Mapped[int] = mapped_column(Integer, default=0)

    user: Mapped["User"] = relationship("User", foreign_keys=[user_id])
    user_ip_address: Mapped[Optional["UserIpAddress"]] = relationship("UserIpAddress", foreign_keys=[user_ip_address_id])
