import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column, relationship


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class SoftDeleteMixin:
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    deleted_by: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    @declared_attr
    def deleted_by_user(cls) -> Mapped[Optional["User"]]:
        return relationship("User", foreign_keys=[cls.deleted_by])


class Base(DeclarativeBase):
    pass
