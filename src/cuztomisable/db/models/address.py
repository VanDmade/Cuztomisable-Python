import uuid
from typing import Optional

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cuztomisable.db.base import Base, SoftDeleteMixin, TimestampMixin


class Address(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "addresses"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    address: Mapped[Optional[str]] = mapped_column(String(), nullable=True)
    address_two: Mapped[Optional[str]] = mapped_column(String(), nullable=True)
    address_three: Mapped[Optional[str]] = mapped_column(String(), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    state_or_province: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    zip_or_postal_code: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    is_default: Mapped[bool] = mapped_column('default', Boolean, default=False)
    shipping: Mapped[bool] = mapped_column(Boolean, default=False)
    billing: Mapped[bool] = mapped_column(Boolean, default=False)

    created_by_user: Mapped[Optional["User"]] = relationship("User", foreign_keys=[created_by])
    user: Mapped["User"] = relationship("User", foreign_keys=[user_id], back_populates="addresses")
