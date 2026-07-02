import uuid
from typing import Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cuztomisable.db.base import Base, TimestampMixin


class EmailLog(TimestampMixin, Base):
    __tablename__ = "email_logs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    to: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    cc: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    bcc: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    from_address: Mapped[Optional[str]] = mapped_column('from', String(128), nullable=True)
    subject: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    parameters: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    created_by_user: Mapped[Optional["User"]] = relationship("User", foreign_keys=[created_by])
