import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cuztomisable.db.base import Base

if TYPE_CHECKING:
    from cuztomisable.db.models.users.user import User


class Image(Base):
    __tablename__ = "images"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    deleted_by: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    created_from_image_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("images.id", ondelete="SET NULL"), nullable=True)
    name: Mapped[str] = mapped_column(String(64))
    extension: Mapped[str] = mapped_column(String(4))
    path: Mapped[str] = mapped_column(String(1024))
    disk: Mapped[str] = mapped_column(String(64))
    parameters: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    original: Mapped[bool] = mapped_column(Boolean, default=True)
    removed_from_storage_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship("User", foreign_keys=[user_id], back_populates="images")
