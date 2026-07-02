import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cuztomisable.db.base import Base, SoftDeleteMixin, TimestampMixin

if TYPE_CHECKING:
    from cuztomisable.db.models.users.user import User


class Role(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "roles"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    name: Mapped[str] = mapped_column(String(128))
    slug: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_by_user: Mapped[Optional["User"]] = relationship("User", foreign_keys=[created_by])
