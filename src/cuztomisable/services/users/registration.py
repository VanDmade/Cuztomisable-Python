import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy.orm import Session

from cuztomisable.db.models.users.registration import UserRegistration

_CODE_EXPIRY = timedelta(days=7)


class UserRegistrationService:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user(self, user_id: uuid.UUID):
        pass

    def get_by_token(self, token: str):
        pass

    def get_by_code(self, code: str) -> Optional[UserRegistration]:
        return (
            self.db.query(UserRegistration)\
                .filter(UserRegistration.code == code)
                .first()
        )

    def get_by_email_or_phone(
        self,
        email: str,
        phone: str = None
    ) -> Optional[UserRegistration]:
        # Finds registrations that match without a code to remove orphaned rows.
        query = self.db.query(UserRegistration).filter(UserRegistration.email == email)
        if phone:
            query = query.filter(UserRegistration.phone == phone)
        return query.first()

    def create(self, data: dict) -> UserRegistration:
        registration = UserRegistration(
            **data,
            code=secrets.token_hex(8),
            expires_at=datetime.now(timezone.utc) + _CODE_EXPIRY,
        )
        self.db.add(registration)
        self.db.flush()
        return registration

    def update(self, registration_id: uuid.UUID, data: dict):
        pass

    def delete(self, registration_id: uuid.UUID):
        pass
