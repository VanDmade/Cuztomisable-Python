import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cuztomisable.db.base import Base, SoftDeleteMixin, TimestampMixin


class Phone(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "phones"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    number: Mapped[str] = mapped_column(String(13))
    country_code: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)
    extension: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)
    mobile: Mapped[bool] = mapped_column(Boolean, default=False)
    is_default: Mapped[bool] = mapped_column('default', Boolean, default=False)
    verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    disable_messages: Mapped[bool] = mapped_column(Boolean, default=False)

    created_by_user: Mapped[Optional["User"]] = relationship("User", foreign_keys=[created_by])
    user: Mapped["User"] = relationship("User", foreign_keys=[user_id])
