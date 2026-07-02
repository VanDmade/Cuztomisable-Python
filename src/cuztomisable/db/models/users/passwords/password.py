import uuid
from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cuztomisable.db.base import Base, TimestampMixin


class UserPassword(TimestampMixin, Base):
    __tablename__ = "user_passwords"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    password: Mapped[str] = mapped_column(String(64))

    created_by_user: Mapped[Optional["User"]] = relationship("User", foreign_keys=[created_by])
    user: Mapped["User"] = relationship("User", foreign_keys=[user_id])
