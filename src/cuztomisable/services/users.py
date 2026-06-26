import uuid

from sqlalchemy.orm import Session


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        pass

    def get_by_id(self, user_id: uuid.UUID):
        pass

    def get_by_email(self, email: str):
        pass

    def create(self, data: dict):
        pass

    def update(self, user_id: uuid.UUID, data: dict):
        pass

    def delete(self, user_id: uuid.UUID):
        pass
