import uuid
from typing import Optional

from sqlalchemy.orm import Session

from cuztomisable.db.models.users.registration import UserRegistration


class UserRegistrationService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user(self, user_id: uuid.UUID):
        pass

    def get_by_token(self, token: str):
        pass

    def get_by_code(self, code: str) -> Optional[UserRegistration]:
        return self.db.query(UserRegistration).filter(UserRegistration.code == code).first()

    def create(self, data: dict):
        pass

    def update(self, registration_id: uuid.UUID, data: dict):
        pass

    def delete(self, registration_id: uuid.UUID):
        pass
