import uuid
from typing import Optional

from sqlalchemy.orm import Session

from cuztomisable.db.models.roles.role_permission import RolePermission
from cuztomisable.schemas.roles.permission import RolePermissionCreate


class RolePermissionService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_role(self, role_id: uuid.UUID) -> list[RolePermission]:
        return (
            self.db.query(RolePermission)
            .filter(RolePermission.role_id == role_id, RolePermission.deleted_at.is_(None))
            .all()
        )

    def get_by_id(self, role_permission_id: uuid.UUID) -> Optional[RolePermission]:
        return (
            self.db.query(RolePermission)
            .filter(RolePermission.id == role_permission_id)
            .first()
        )

    def create(self, role_id: uuid.UUID, data: RolePermissionCreate) -> RolePermission:
        rp = RolePermission(role_id=role_id, **data.model_dump())
        self.db.add(rp)
        self.db.commit()
        self.db.refresh(rp)
        return rp

    def delete(self, role_permission_id: uuid.UUID) -> bool:
        rp = self.get_by_id(role_permission_id)
        if not rp:
            return False
        self.db.delete(rp)
        self.db.commit()
        return True
