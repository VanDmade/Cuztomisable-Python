import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cuztomisable.db.base import Base

if TYPE_CHECKING:
    from cuztomisable.db.models.image import Image
    from cuztomisable.db.models.phone import Phone
    from cuztomisable.db.models.address import Address
    from cuztomisable.db.models.permission import Permission
    from cuztomisable.db.models.roles.role import Role
    from cuztomisable.db.models.users.permission import UserPermission
    from cuztomisable.db.models.users.ip_address import UserIpAddress
    from cuztomisable.db.models.users.code import UserCode
    from cuztomisable.db.models.users.registration import UserRegistration
    from cuztomisable.db.models.users.passwords.password import UserPassword
    from cuztomisable.db.models.users.passwords.reset import UserPasswordReset
    from cuztomisable.db.models.users.tokens.access import UserAccessToken
    from cuztomisable.db.models.users.tokens.refresh import UserRefreshToken


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    deleted_by: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    image_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("images.id", use_alter=True, name="fk_users_image_id", ondelete="SET NULL"), nullable=True
    )
    role_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("roles.id", ondelete="SET NULL"), nullable=True)
    name: Mapped[str] = mapped_column(String(128))
    username: Mapped[Optional[str]] = mapped_column(String(128), unique=True, index=True, nullable=True)
    email: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    email_verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    disable_emails: Mapped[bool] = mapped_column(Boolean, default=False)
    password: Mapped[str] = mapped_column(String(64))
    timezone: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    locked: Mapped[bool] = mapped_column(Boolean, default=False)
    change_password: Mapped[bool] = mapped_column(Boolean, default=False)
    change_password_sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    multi_factor_authentication: Mapped[bool] = mapped_column(Boolean, default=False)
    admin: Mapped[bool] = mapped_column(Boolean, default=False)
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    attempt_timer: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    token: Mapped[Optional[str]] = mapped_column(String(32), unique=True, nullable=True)

    image: Mapped[Optional["Image"]] = relationship("Image", foreign_keys=[image_id], post_update=True)
    images: Mapped[List["Image"]] = relationship(
        "Image", foreign_keys="Image.user_id", back_populates="user", cascade="all, delete-orphan"
    )

    role: Mapped[Optional["Role"]] = relationship("Role", foreign_keys=[role_id])

    user_permissions: Mapped[List["UserPermission"]] = relationship(
        "UserPermission", foreign_keys="UserPermission.user_id", cascade="all, delete-orphan"
    )
    permissions: Mapped[List["Permission"]] = relationship(
        "Permission", secondary="user_permissions", viewonly=True
    )

    phones: Mapped[List["Phone"]] = relationship(
        "Phone", foreign_keys="Phone.user_id", cascade="all, delete-orphan"
    )
    addresses: Mapped[List["Address"]] = relationship(
        "Address", foreign_keys="Address.user_id", cascade="all, delete-orphan"
    )
    ip_addresses: Mapped[List["UserIpAddress"]] = relationship(
        "UserIpAddress", foreign_keys="UserIpAddress.user_id", cascade="all, delete-orphan"
    )
    codes: Mapped[List["UserCode"]] = relationship(
        "UserCode", foreign_keys="UserCode.user_id", cascade="all, delete-orphan"
    )
    registrations: Mapped[List["UserRegistration"]] = relationship(
        "UserRegistration", foreign_keys="UserRegistration.user_id", cascade="all, delete-orphan"
    )
    passwords: Mapped[List["UserPassword"]] = relationship(
        "UserPassword", foreign_keys="UserPassword.user_id", cascade="all, delete-orphan"
    )
    password_resets: Mapped[List["UserPasswordReset"]] = relationship(
        "UserPasswordReset", foreign_keys="UserPasswordReset.user_id", cascade="all, delete-orphan"
    )
    access_tokens: Mapped[List["UserAccessToken"]] = relationship(
        "UserAccessToken", foreign_keys="UserAccessToken.user_id", cascade="all, delete-orphan"
    )
    refresh_tokens: Mapped[List["UserRefreshToken"]] = relationship(
        "UserRefreshToken", foreign_keys="UserRefreshToken.user_id", cascade="all, delete-orphan"
    )
