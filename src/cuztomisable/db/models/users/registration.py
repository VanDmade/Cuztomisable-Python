import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cuztomisable.db.base import Base, SoftDeleteMixin, TimestampMixin


class UserRegistration(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "user_registrations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    name: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(15), nullable=True)
    code: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    used_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    attempt_counter: Mapped[int] = mapped_column(Integer, default=0)

    created_by_user: Mapped[Optional["User"]] = relationship("User", foreign_keys=[created_by])
    user: Mapped[Optional["User"]] = relationship("User", foreign_keys=[user_id])
