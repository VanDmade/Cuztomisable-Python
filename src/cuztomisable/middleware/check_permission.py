from fastapi import Depends, status
from sqlalchemy.orm import Session

from cuztomisable.db.models.permission import Permission
from cuztomisable.db.models.roles.role_permission import RolePermission
from cuztomisable.db.models.users.permission import UserPermission
from cuztomisable.db.models.users.user import User
from cuztomisable.exceptions import CuztomisableException
from cuztomisable.helpers.dependencies import get_current_user, get_db
from cuztomisable.lang import trans


def _has_permission(user: User, slug: str, db: Session) -> bool:
    if user.admin:
        return True

    # Check direct user permissions
    direct = (
        db.query(UserPermission)
            .join(Permission, Permission.id == UserPermission.permission_id)
            .filter(
                UserPermission.user_id == user.id,
                UserPermission.deleted_at.is_(None),
                Permission.slug == slug,
            )
            .first()
    )

    if direct:
        return True

    # Check role permissions
    if user.role_id:
        via_role = (
            db.query(RolePermission)
                .join(Permission, Permission.id == RolePermission.permission_id)
                .filter(
                    RolePermission.role_id == user.role_id,
                    RolePermission.deleted_at.is_(None),
                    Permission.slug == slug,
                )
                .first()
        )

        if via_role:
            return True

    return False


def require_permission(permissions: str):
    """
    Dependency factory for permission checking.

    Usage:
        # Single permission
        Depends(require_permission("roles.view"))

        # OR — user needs at least one
        Depends(require_permission("roles.view|roles.manage"))

        # AND — user needs all
        Depends(require_permission("roles.view,roles.manage"))
    """
    def dependency(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> User:
        forbidden = CuztomisableException(
            code=status.HTTP_403_FORBIDDEN,
            message=trans("global.errors.unauthorized"),
            key="forbidden",
        )

        if "|" in permissions:
            perms = [p.strip() for p in permissions.split("|") if p.strip()]
            if not any(_has_permission(current_user, p, db) for p in perms):
                raise forbidden

        elif "," in permissions:
            perms = [p.strip() for p in permissions.split(",") if p.strip()]
            if not all(_has_permission(current_user, p, db) for p in perms):
                raise forbidden

        else:
            if not _has_permission(current_user, permissions.strip(), db):
                raise forbidden

        return current_user

    return dependency
