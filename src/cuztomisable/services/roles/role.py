import uuid
from typing import Optional

from sqlalchemy.orm import Session, joinedload

from cuztomisable.db.models.roles.role import Role
from cuztomisable.schemas.roles.role import RoleCreate, RoleUpdate


class RoleService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[Role]:
        return (
            self.db.query(Role)
                .options(joinedload(Role.created_by_user))
                .filter(Role.deleted_at.is_(None))
                .all()
        )

    def get_by_id(self, role_id: uuid.UUID) -> Optional[Role]:
        return (
            self.db.query(Role)
                .options(joinedload(Role.created_by_user))
                .filter(Role.id == role_id, Role.deleted_at.is_(None))
                .first()
        )

    def get_by_slug(self, slug: str) -> Optional[Role]:
        return (
            self.db.query(Role)
                .options(joinedload(Role.created_by_user))
                .filter(Role.slug == slug, Role.deleted_at.is_(None))
                .first()
        )

    def create(self, data: RoleCreate) -> Role:
        role = Role(**data.model_dump())
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role

    def update(self, role_id: uuid.UUID, data: RoleUpdate) -> Optional[Role]:
        role = self.get_by_id(role_id)
        if not role:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(role, key, value)
        self.db.commit()
        self.db.refresh(role)
        return role

    def delete(self, role_id: uuid.UUID) -> bool:
        role = self.get_by_id(role_id)
        if not role:
            return False
        self.db.delete(role)
        self.db.commit()
        return True
