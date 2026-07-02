import uuid
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cuztomisable.db.base import Base, SoftDeleteMixin, TimestampMixin


class RolePermission(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "role_permissions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    role_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"), index=True)
    permission_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("permissions.id", ondelete="CASCADE"))

    created_by_user: Mapped[Optional["User"]] = relationship("User", foreign_keys=[created_by])
    role: Mapped["Role"] = relationship("Role", foreign_keys=[role_id])
    permission: Mapped["Permission"] = relationship("Permission", foreign_keys=[permission_id])
