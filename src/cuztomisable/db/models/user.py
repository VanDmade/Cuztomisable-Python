import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cuztomisable.db.base import Base

if TYPE_CHECKING:
    from .image import Image


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    username: Mapped[Optional[str]] = mapped_column(String(100), unique=True, index=True, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    # Profile image — use_alter avoids circular FK with images table
    image_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("images.id", use_alter=True, name="fk_users_image_id", ondelete="SET NULL"),
        nullable=True,
    )

    # Audit fields
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    deleted_by: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    image: Mapped[Optional["Image"]] = relationship(
        "Image", foreign_keys=[image_id], post_update=True
    )
    images: Mapped[List["Image"]] = relationship(
        "Image", foreign_keys="Image.user_id", back_populates="user", cascade="all, delete-orphan"
    )
