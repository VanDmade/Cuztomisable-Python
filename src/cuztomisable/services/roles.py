import uuid

from sqlalchemy.orm import Session


class RoleService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        pass

    def get_by_id(self, role_id: uuid.UUID):
        pass

    def create(self, data: dict):
        pass

    def update(self, role_id: uuid.UUID, data: dict):
        pass

    def delete(self, role_id: uuid.UUID):
        pass
