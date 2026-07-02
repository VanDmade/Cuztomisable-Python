import uuid
from typing import Optional

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cuztomisable.db.base import Base, TimestampMixin


class ErrorLog(TimestampMixin, Base):
    __tablename__ = "error_logs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    line: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    file: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    code: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)
    debug_code: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)
    parameters: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    user: Mapped[Optional["User"]] = relationship("User", foreign_keys=[user_id])
