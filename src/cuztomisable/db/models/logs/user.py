import uuid
from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cuztomisable.db.base import Base, TimestampMixin


class UserLog(TimestampMixin, Base):
    __tablename__ = "user_logs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    description: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    parameters: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    created_by_user: Mapped[Optional["User"]] = relationship("User", foreign_keys=[created_by])
    user: Mapped["User"] = relationship("User", foreign_keys=[user_id], back_populates="user_logs")
