import uuid

from sqlalchemy.orm import Session


class UserAccessTokenService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user(self, user_id: uuid.UUID):
        pass

    def get_by_token(self, token: str):
        pass

    def create(self, user_id: uuid.UUID, data: dict):
        pass

    def delete(self, token_id: uuid.UUID):
        pass
