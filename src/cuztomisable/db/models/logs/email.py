import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from cuztomisable.db.base import Base


class EmailLog(Base):
    __tablename__ = "email_logs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    to: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    cc: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    bcc: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    from_address: Mapped[Optional[str]] = mapped_column('from', String(128), nullable=True)
    subject: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    parameters: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
