import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from cuztomisable.db.base import Base


class TextLog(Base):
    __tablename__ = "text_logs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    number: Mapped[Optional[str]] = mapped_column(String(13), nullable=True)
    country_code: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)
    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    parameters: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
