import uuid

from sqlalchemy.orm import Session


class UserRegistrationService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user(self, user_id: uuid.UUID):
        pass

    def get_by_token(self, token: str):
        pass

    def create(self, data: dict):
        pass

    def update(self, registration_id: uuid.UUID, data: dict):
        pass

    def delete(self, registration_id: uuid.UUID):
        pass
