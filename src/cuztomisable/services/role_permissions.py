import uuid

from sqlalchemy.orm import Session


class RolePermissionService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_role(self, role_id: uuid.UUID):
        pass

    def create(self, role_id: uuid.UUID, data: dict):
        pass

    def delete(self, role_permission_id: uuid.UUID):
        pass
