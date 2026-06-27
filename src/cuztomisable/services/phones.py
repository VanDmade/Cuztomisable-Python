import uuid

from sqlalchemy.orm import Session


class PhoneService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user(self, user_id: uuid.UUID):
        pass

    def get_by_id(self, phone_id: uuid.UUID):
        pass

    def create(self, user_id: uuid.UUID, data: dict):
        pass

    def update(self, phone_id: uuid.UUID, data: dict):
        pass

    def delete(self, phone_id: uuid.UUID):
        pass
