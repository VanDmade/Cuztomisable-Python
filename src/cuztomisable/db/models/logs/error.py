import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from cuztomisable.db.base import Base


class ErrorLog(Base):
    __tablename__ = "error_logs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    line: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    file: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    code: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)
    debug_code: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)
    parameters: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
