import uuid

from sqlalchemy.orm import Session


class PermissionService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        pass

    def get_by_id(self, permission_id: uuid.UUID):
        pass

    def create(self, data: dict):
        pass

    def update(self, permission_id: uuid.UUID, data: dict):
        pass

    def delete(self, permission_id: uuid.UUID):
        pass
